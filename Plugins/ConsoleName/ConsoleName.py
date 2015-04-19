__title__ = 'ConsoleName'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class ConsoleName:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("ConsoleName", "ConsoleName", "Pluton")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        Server.server_message_name = ini.GetSetting("ConsoleName", "ConsoleName")

    def On_Command(self, command):
        if command.cmd == "consolename":
            Player = command.User
            if Player.Owner or Player.Admin:
                if len(command.args) == 0:
                    command.User.Message("Usage: /consolename [console name]")
                else:
                    name = str.Join(" ", command.args)
                    if name == "":
                        command.User.Message("Usage: /consolename [console name]")
                        return
                    else:
                        ini = Plugin.GetIni("Settings")
                        ini.DeleteSetting("ConsoleName", "ConsoleName")
                        ini.AddSetting("ConsoleName", "ConsoleName", name)
                        ini.Save()
                        Server.server_message_name = name
                        command.User.MessageFrom(name, " is the new ConsoleName!")
            else:
                command.User.MessageFrom("ConsoleName", "You are not allowed to use that command")
