# tts-asset-reuploader

Sometimes, URLs used in Tabletop Simulator games go down. If you have the file in your local cache, the objects will still work for you, but not for others. If you run this script aimed at a TTS save game (.json file), it will attempt to retrieve all the URLs within that game that point at the steam cloud servers. For any URLs that return 404 Not Found, if you have that file in your local cache, it will rewrite that URL in your save game to point to your local cache. Then, you can reload that save game in TTS, and use the TTS built in mechanism to mass upload all the local files to the cloud (Modding -> Cloud Manager -> little up arrow "Upload All Loaded Files"), and resave.

The above paragraph in numbered instructions:

1. Have Python installed if you haven't already.
2. Run the script aimed at one of your save files, via the command line:
   ```
   python tts_asset_reuploader.py "C:\path\to\your\savegame.json"
   ```
   (this can take a little while if there are a lot of URLs to fetch)
3. Reopen the save game in Tabletop Simulator
4. Upload All Loaded Files (Modding -> Cloud Manager -> little up arrow "Upload All Loaded Files") (this can take a while if there are many items to upload).
5. Save game.
