__title__ = 'Rules'
__author__ = 'Jakkee'
__version__ = '1.0.3'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class Rules:
    def On_PluginInit(self):
        if not Plugin.IniExists("Rules"):
            Plugin.CreateIni("Rules")
            ini = Plugin.GetIni("Rules")
            ini.AddSetting("Settings", "ChatName", "Pluton")
            ini.AddSetting("Rules", "0", "Server Rules;")
            ini.AddSetting("Rules", "1", "1: Any form of cheating/glitching is not allowed")
            ini.AddSetting("Rules", "2", "2: Realistic building, no floating buildings etc")
            ini.AddSetting("Rules", "3", "3: Do not spam chat or deployable objects")
            ini.Save()
        ini = Plugin.GetIni("Rules")
        DataStore.Add("Rules", "ServerName", ini.GetSetting("Settings", "ChatName"))

    def On_Command(self, command):
        if command.cmd == "rules":
            Player = command.User
            ini = Plugin.GetIni("Rules")
            rules = ini.EnumSection("Rules")
            name = DataStore.Get("Rules", "ServerName")
            for rule in rules:
                Player.MessageFrom(name, ini.GetSetting("Rules", rule))
