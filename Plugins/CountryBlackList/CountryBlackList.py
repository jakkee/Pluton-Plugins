__title__ = 'CountryBlackList'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class CountryBlackList:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "ShowAcceptedMessage", "true")
            ini.AddSetting("Settings", "ShowDeniedMessage", "true")
            ini.AddSetting("Settings", "LogTimedOutConnection", "true")
            ini.AddSetting("BlackList", "BlackListedCountries", "TK, JO")
            ini.AddSetting("Messages", "JoinMessage", "%PLAYER% has connected from: %COUNTRY%")
            ini.AddSetting("Messages", "PlayerDisconnectMessage", "Your country is on the servers blacklist")
            ini.AddSetting("Messages", "DisconnectMessage", "%PLAYER% is trying to connect from: %COUNTRY% but is black listed")
            ini.AddSetting("Messages", "UnknownLocation", "A hidden location")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("CountryBlackList", "SAM", ini.GetSetting("Settings", "ShowAcceptedMessage"))
        DataStore.Add("CountryBlackList", "SDM", ini.GetSetting("Settings", "ShowDeniedMessage"))
        DataStore.Add("CountryBlackList", "LTOC", ini.GetSetting("Settings", "LogTimedOutConnection"))
        DataStore.Add("CountryBlackList", "BL", ini.GetSetting("BlackList", "BlackListedCountries"))
        DataStore.Add("CountryBlackList", "JM", ini.GetSetting("Messages", "JoinMessage"))
        DataStore.Add("CountryBlackList", "PDM", ini.GetSetting("Messages", "PlayerDisconnectMessage"))
        DataStore.Add("CountryBlackList", "DM", ini.GetSetting("Messages", "DisconnectMessage"))
        DataStore.Add("CountryBlackList", "UL", ini.GetSetting("Messages", "UnknownLocation"))

    def find(self, b, c):
        try:
            #Throws an error if website timed out (Because c has no string)
            b = b.Replace(" ", "")
            b = b.split(',')
            c = c[:-1]
            for a in b:
                if c == a:
                    return True
            return False
        except:
            return False

    def splitip(self, ip):
        ip = ip.split(":")
        return ip

    def getcountry(self, Name, IP, ID):
        IP = self.splitip(IP)
        try:
            if IP[0] == "127.0.0.1":
                return DataStore.Get("CountryBlackList", "UL")
            country = Web.GET("http://ipinfo.io/" + IP[0] + "/country")
            if country == "undefined":
                return DataStore.Get("CountryBlackList", "UL")
            return country
        except:
            if DataStore.Get("CountryBlackList", "SDM") == "true":
                msg = DataStore.Get("CountryBlackList", "JM")
                msg = msg.Replace("%PLAYER%", Name)
                msg = msg.Replace("%COUNTRY%", DataStore.Get("CountryBlackList", "UL"))
                Server.Broadcast(msg)
            if DataStore.Get("CountryBlackList", "LTOC") == "true":
                if not Plugin.IniExists("ConnectionLog"):
                    Plugin.CreateIni("ConnectionLog")
                    log = Plugin.GetIni("ConnectionLog")
                    log.Save()
                log = Plugin.GetIni("ConnectionLog")
                log.AddSetting("Timed out connections", Plugin.GetDate() + "|" + Plugin.GetTime() + " ", " SteamID: " + str(ID) + ". Name: " + Name + ". IP: " + IP[0])
                log.Save()
            pass

    def On_ClientAuth(self, AuthEvent):
        try:
            bl = DataStore.Get("CountryBlackList", "BL")
            c = self.getcountry(AuthEvent.Name, AuthEvent.IP, AuthEvent.GameID)
            if self.find(bl, c):
                pdis = DataStore.Get("CountryBlackList", "PDM")
                AuthEvent.Reject(pdis + " [" + c + "]")
                if DataStore.Get("CountryBlackList", "SAM") == "true":
                    msg = DataStore.Get("CountryBlackList", "DM")
                    msg = msg.Replace("%PLAYER%", AuthEvent.Name)
                    msg = msg.Replace("%COUNTRY%", c)
                    Server.Broadcast(msg)
            else:
                if DataStore.Get("CountryBlackList", "SAM") == "true":
                    msg = DataStore.Get("CountryBlackList", "JM")
                    msg = msg.Replace("%PLAYER%", AuthEvent.Name)
                    msg = msg.Replace("%COUNTRY%", c)
                    Server.Broadcast(msg)
        except:
            pass
