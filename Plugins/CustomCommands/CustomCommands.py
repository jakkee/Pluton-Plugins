__title__ = 'CustomCommands'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class CustomCommands:
    def On_PluginInit(self):
        if not Plugin.IniExists("Commands"):
            Plugin.CreateIni("Commands")
            ini = Plugin.GetIni("Commands")
            ini.AddSetting("CustomCommands", "/vote", "vote for us at: http://SomeVotingAddress.com")
            ini.AddSetting("CustomCommands", "/website", "Our website: http://google.com")
            ini.AddSetting("CustomCommands", "/test", " - This is a test")
            ini.AddSetting("CustomCommands", "/teamspeak", "Teamspeak IP: 111.111.111:0000")
            ini.AddSetting("CustomCommands", "/donate", "Talk to a staff member about donating")
            ini.Save()
        DataStore.Flush("CustomCommands")
        ini = Plugin.GetIni("Commands")
        for command in ini.EnumSection("CustomCommands"):
            cmd = command.replace("/", "")
            DataStore.Add("CustomCommands", cmd, ini.GetSetting("CustomCommands", command))

    def On_Command(self, CommandEvent):
        if not DataStore.Get("CustomCommands", CommandEvent.cmd) is None:
            message = DataStore.Get("CustomCommands", CommandEvent.cmd)
            CommandEvent.User.Message(message)
