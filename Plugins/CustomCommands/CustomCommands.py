__title__ = 'CustomCommands'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
import Pluton
import UnityEngine


class CustomCommands:
    def On_PluginInit(self):
        if not Plugin.IniExists("Commands"):
            Plugin.CreateIni("Commands")
            ini = Plugin.GetIni("Commands")
            ini.AddSetting("Website", "/website", "http://Fougerite.com")
            ini.AddSetting("Website", "/google", "http://google.com")
            ini.AddSetting("Info", "/test", " - This is a test")
            ini.AddSetting("Info", "/teamspeak", "Teamspeak IP: 423.723.478:0000")
            ini.AddSetting("Info", "/motd", "Talk to a staff member about donating")
            ini.Save()
        ini = Plugin.GetIni("Commands")
        for command in ini.EnumSection("Website"):
            cmd = command.replace("/", "")
            DataStore.Add("CustomCommands", cmd + "Type", "Website")
            DataStore.Add("CustomCommands", cmd, ini.GetSetting("Website", command))
        for command in ini.EnumSection("Info"):
            cmd = command.replace("/", "")
            DataStore.Add("CustomCommands", cmd + "Type", "Info")
            DataStore.Add("CustomCommands", cmd, ini.GetSetting("Info", command))

    def On_Command(self, ce):
        if DataStore.Get("CustomCommands", ce.cmd + "Type") == "Website":
            if DataStore.Get("CustomCommands", ce.cmd) is not None:
                website = DataStore.Get("CustomCommands", ce.cmd)
                ce.User.Message("Opening website: " + website + " in your web browser")
                UnityEngine.Application.OpenURL(website)
        elif DataStore.Get("CustomCommands", ce.cmd + "Type") == "Info":
            if DataStore.Get("CustomCommands", ce.cmd) is not None:
                message = DataStore.Get("CustomCommands", ce.cmd)
                ce.User.Message(message)
