__title__ = 'CountryBlackList'
__author__ = 'Jakkee'
__about__ = 'Blacklist countries'
__version__ = '1.1.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import System


class CountryBlackList:

    GeoIP = None
    
    def On_PluginInit(self):
        if Plugin.GetPlugin("GeoIP") is None:
            raise ImportError("Failed to reference the GeoIP.dll, Download from: http://forum.pluton-team.org/threads/geoip.437/")
        self.GeoIP = Plugin.GetPlugin("GeoIP")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "ShowAcceptedMessage", "true")
            ini.AddSetting("Settings", "ShowDeniedMessage", "true")
            ini.AddSetting("Settings", "LogTimedOutConnection", "true")
            ini.AddSetting("BlackList", "BlackListedCountries", "TK, JO")
            ini.AddSetting("Messages", "JoinMessage", "%PLAYER% has connected from: %COUNTRY%")
            ini.AddSetting("Messages", "PlayerDisconnectMessage", "Your country is on the servers blacklist")
            ini.AddSetting("Messages", "ServerDisconnectMessage", "%PLAYER% is trying to connect from: %COUNTRY% but is black listed")
            ini.AddSetting("Messages", "UnknownLocation", "A hidden location")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("CountryBlackList", "SAM", ini.GetSetting("Settings", "ShowAcceptedMessage"))
        DataStore.Add("CountryBlackList", "SDM", ini.GetSetting("Settings", "ShowDeniedMessage"))
        DataStore.Add("CountryBlackList", "BL", ini.GetSetting("BlackList", "BlackListedCountries"))
        DataStore.Add("CountryBlackList", "JM", ini.GetSetting("Messages", "JoinMessage"))
        DataStore.Add("CountryBlackList", "PDM", ini.GetSetting("Messages", "PlayerDisconnectMessage"))
        DataStore.Add("CountryBlackList", "DM", ini.GetSetting("Messages", "ServerDisconnectMessage"))
        DataStore.Add("CountryBlackList", "UL", ini.GetSetting("Messages", "UnknownLocation"))
        countrycode = Plugin.GetPlugin("GeoIP").Engine.GetDataOfIP("123.2.112.41").CountryShort
        Util.Log(countrycode)
        #

    def find(self, blacklist, CountryCode):
        try:
            blacklist = blacklist.Replace(" ", "")
            blacklist = blacklist.split(',')
            for configlist in b:
                if CountryCode == configlist:
                    return True
                else:
                    continue
            return False
        except:
            return False

    def On_PlayerConnected(self, Player):
        #try:
        countrycode = Plugin.GetPlugin("GeoIP").Engine.GetDataOfIP("123.2.112.41").CountryShort
        Util.Log(countrycode)
        blacklist = DataStore.Get("CountryBlackList", "BL")
        if self.find(blacklist, countrycode):
            playerdisconnectMSG = DataStore.Get("CountryBlackList", "PDM")
            if DataStore.Get("CountryBlackList", "SDM") == "true":
                msg = DataStore.Get("CountryBlackList", "DM")
                msg = msg.Replace("%PLAYER%", Player.Name)
                msg = msg.Replace("%COUNTRY%", IPData.Country)
                Server.Broadcast(msg)
            Player.Kick(playerdisconnectMSG + " [" + countrycode + "]")
        else:
            if DataStore.Get("CountryBlackList", "SAM") == "true":
                msg = DataStore.Get("CountryBlackList", "JM")
                msg = msg.Replace("%PLAYER%", Player.Name)
                msg = msg.Replace("%COUNTRY%", IPData.Country)
                Server.Broadcast(msg)
        #except Exception, error:
            #Util.Log(error[0])
            #if DataStore.Get("CountryBlackList", "SAM") == "true":
                #msg = DataStore.Get("CountryBlackList", "JM")
                #msg = msg.Replace("%PLAYER%", Player.Name)
                #msg = msg.Replace("%COUNTRY%", DataStore.Get("CountryBlackList", "UL"))
                #Server.Broadcast(msg)
