"""

"""

import collections
import json
import multiprocessing
import os
import pathlib
import random
import re
import requests
import sys
import sqlite3
import time
from time import gmtime, strftime

# If your Tabletop Simulator data directory is in some alternative location,
# paste it in the quotes below.
TTS_DIR_OVERRIDE = r""


def tts_default_locations():
    """Attempt to guess the Tabletop Simulator data directory."""
    if sys.platform == "linux" or sys.platform == "linux2":
        return [
            os.path.join(
                str(pathlib.Path.home()),
                ".local",
                "share",
                "Tabletop Simulator",
            )
        ]
    elif sys.platform == "darwin":  # mac osx
        return [os.path.join(str(pathlib.Path.home()), "Library", "Tabletop Simulator")]
    elif sys.platform == "win32":
        return [
            os.path.join(
                os.environ["USERPROFILE"],
                "Documents",
                "My Games",
                "Tabletop Simulator",
            ),
            os.path.join(
                os.environ["USERPROFILE"],
                "OneDrive",
                "Documents",
                "My Games",
                "Tabletop Simulator",
            ),
        ]
    else:
        return [
            f"couldn't match platform {sys.platform}, so don't know save game location"
        ]


class CachedThing:
    def __init__(self, full_path):
        self.full_path = full_path
        self.basename = os.path.basename(full_path)

    def matches_re(self, regexstr):
        if not regexstr:
            return False
        return bool(re.match(regexstr, self.basename))


def url_in_cache_re(url):
    """Returns a regex string that should match the file in the cache
    that would correspond to the URL. I don't know the precise format
    that TTS uses, and I know the steamusercontent has moved at least
    once, so that's why it's a regex not just a literal string exact
    match."""
    r = "^http.*steamusercontent.*/([a-fA-F0-9]{15,25})/([a-fA-F0-9]{30,50})/?$"
    m = re.match(r, url)
    if not m:
        return re.sub("[^a-zA-Z0-9]", ".?", url)
    return ".*steamusercontent.*" + m.group(1) + ".?" + m.group(2) + ".*"


def retriably_rename(old_path, new_path):
    """Retriably move something from path to path.

    This exists just as a possible workaround for an issue on my
    remote drive.
    """
    for ix in range(5):
        try:
            os.rename(old_path, new_path)
            return
        except PermissionError:
            time.sleep(2.0)
    # last ditch attempt
    os.rename(old_path, new_path)


def read_file(filename):
    infile = open(filename, mode="r", encoding="utf-8")
    intext = infile.read()
    infile.close()
    return intext


def get_obj_urls(obj):
    l = []
    if isinstance(obj, dict):
        for v in obj.values():
            for u in get_obj_urls(v):
                l.append(u)
    elif isinstance(obj, list):
        for v in obj:
            for u in get_obj_urls(v):
                l.append(u)
    elif isinstance(obj, str):
        if obj.startswith("http") and len(obj) < 2000:
            l.append(obj)
    return l


def replaced_obj_urls(obj, url_replacements):
    if isinstance(obj, dict):
        output = {}
        for k in obj:
            output[k] = replaced_obj_urls(obj[k], url_replacements)
        return output
    elif isinstance(obj, list):
        return [replaced_obj_urls(x, url_replacements) for x in obj]
    elif isinstance(obj, str):
        return url_replacements.get(obj, obj)
    return obj


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TMP_DIR = os.path.join(THIS_DIR, "TMP_DELETE_ME_LATER")
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)


def get_cache_things():
    cache_things = []
    print("Examining TTS cache. If we find zero things, something probably went wrong.")
    for tts_root in tts_default_locations() + [TTS_DIR_OVERRIDE]:
        if not tts_root or not os.path.exists(tts_root):
            continue
        for subdir in [
            "Assetbundles",
            "Audio",
            "Images",
            "Models",
            "PDF",
            "Text",
            "Translations",
        ]:
            full_subdir = os.path.join(tts_root, "Mods", subdir)
            print(full_subdir)
            l = []
            try:
                l = os.listdir(full_subdir)
            except:
                pass
            for x in l:
                cache_things.append(CachedThing(os.path.join(full_subdir, x)))
    print("Found", len(cache_things), "cache things")
    return cache_things


def update_dead_urls(filename, cache_things):
    o = json.loads(read_file(filename))
    urls = sorted(list(set(get_obj_urls(o))))
    print("Found", len(urls), "distinct urls")
    print("Testing URLs")
    status_code_counts = collections.defaultdict(lambda: 0)
    missing_urls = set()
    for u in urls:
        if "steamusercontent" not in u:
            continue
        print(u)
        r = requests.get(u)
        status_code_counts[r.status_code] += 1
        if r.status_code == 200:
            print("ok!")
        elif r.status_code == 404:
            missing_urls.add(u)
            print("not found!")
        else:
            print("weird status:", r.status_code)
    print(status_code_counts)

    url_replacements = {}
    for u in missing_urls:
        r = url_in_cache_re(u)
        matching_cache_things = []
        for c in cache_things:
            if c.matches_re(r):
                matching_cache_things.append(c)
        print("404-ing URL:", u)
        if len(matching_cache_things) >= 1:
            print("Cache location:", matching_cache_things[0].full_path)
            url_replacements[u] = "file:///" + matching_cache_things[0].full_path
    print(
        "Found", len(url_replacements), "things that were 404-ing but we have cached."
    )
    if not url_replacements:
        print(
            "As we found no URLs that are both 404-ing and cached, we won't rewrite the file."
        )
        return

    obj2 = replaced_obj_urls(o, url_replacements)
    now = strftime("%Y-%m-%dT%H-%M-%SZ", gmtime())
    backup_filename = f"{filename}-{now}.backup"
    print("Moving to backup location", backup_filename)
    retriably_rename(filename, backup_filename)
    tmp_filename = f"{filename}.tmp"
    outfile = open(tmp_filename, mode="w")
    json.dump(obj2, outfile, indent=2)
    outfile.close()
    retriably_rename(tmp_filename, filename)
    print("Updated", filename)


if __name__ == "__main__":
    files_to_clean = list(sys.argv[1:])
    cache_things = []
    if files_to_clean:
        cache_things = get_cache_things()
    for filename in files_to_clean:
        update_dead_urls(filename, cache_things)
