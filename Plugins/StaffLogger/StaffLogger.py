__title__ = 'StaffLogger'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import System


class StaffLogger:
    def On_PluginInit(self):
        if not Plugin.IniExists("Log"):
            Plugin.CreateIni("Log")
            Plugin.GetIni("Log").Save()
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("OwnerLog", "Commands", "false")
            ini.AddSetting("OwnerLog", "Chat", "false")
            ini.AddSetting("OwnerLog", "Looting", "false")
            ini.AddSetting("AdminLog", "Commands", "true")
            ini.AddSetting("AdminLog", "Chat", "false")
            ini.AddSetting("AdminLog", "Looting", "true")
            ini.AddSetting("ModeratorLog", "Commands", "true")
            ini.AddSetting("ModeratorLog", "Chat", "false")
            ini.AddSetting("ModeratorLog", "Looting", "true")
            ini.AddSetting("PlayerLog", "Commands", "false")
            ini.AddSetting("PlayerLog", "Chat", "false")
            ini.AddSetting("PlayerLog", "Looting", "true")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("StaffLogger")
        DataStore.Add("StaffLogger", "OwnerCommands", ini.GetSetting("OwnerLog", "Commands"))
        DataStore.Add("StaffLogger", "OwnerChat", ini.GetSetting("OwnerLog", "Chat"))
        DataStore.Add("StaffLogger", "OwnerLooting", ini.GetSetting("OwnerLog", "Looting"))
        DataStore.Add("StaffLogger", "AdminCommands", ini.GetSetting("AdminLog", "Commands"))
        DataStore.Add("StaffLogger", "AdminChat", ini.GetSetting("AdminLog", "Chat"))
        DataStore.Add("StaffLogger", "AdminLooting", ini.GetSetting("AdminLog", "Looting"))
        DataStore.Add("StaffLogger", "ModeratorCommands", ini.GetSetting("ModeratorLog", "Commands"))
        DataStore.Add("StaffLogger", "ModeratorChat", ini.GetSetting("ModeratorLog", "Chat"))
        DataStore.Add("StaffLogger", "ModeratorLooting", ini.GetSetting("ModeratorLog", "Looting"))
        DataStore.Add("StaffLogger", "PlayerCommands", ini.GetSetting("PlayerLog", "Commands"))
        DataStore.Add("StaffLogger", "PlayerChat", ini.GetSetting("PlayerLog", "Chat"))
        DataStore.Add("StaffLogger", "PlayerLooting", ini.GetSetting("PlayerLog", "Looting"))

    def On_Command(self, CommandEvent):
        Player = CommandEvent.User
        arg = self.usercheck(Player, "Command")
        if arg[0]:
            args = self.argsToText(CommandEvent.args)
            ini = Plugin.GetIni("Log")
            ini.AddSetting(arg[1], "[" + str(System.DateTime.Now) + "]", Player.SteamID + "=" + Player.Name + arg[2] + CommandEvent.cmd + " " + args)
            ini.Save()

    def On_Chat(self, ChatEvent):
        Player = ChatEvent.User
        arg = self.usercheck(Player, "Chat")
        if arg[0]:
            ini = Plugin.GetIni("Log")
            ini.AddSetting(arg[1], "[" + str(System.DateTime.Now) + "]", Player.SteamID + "=" + Player.Name + arg[2] + ChatEvent.OriginalText)
            ini.Save()

    """def On_LootingPlayer(self, PlayerLootEvent):
        Player = ChatEvent.User
        arg = self.usercheck(Player, "Chat")
        if arg[0]:
            ini = Plugin.GetIni("Log")
            ini.AddSetting(arg[1], "[" + str(System.DateTime.Now) + "]", Player.SteamID + "=" + Player.Name + arg[2] + ChatEvent.OriginalText)
            ini.Save()"""

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def usercheck(self, Player, typee):
        if typee == "Command":
            if Player.Owner:
                if DataStore.Get("StaffLogger", "OwnerCommands") == "true":
                    return True, "OwnerLog", " typed: /"
                else:
                    return False, None, None
            elif Player.Admin:
                if DataStore.Get("StaffLogger", "AdminCommands") == "true":
                    return True, "AdminLog", " typed: /"
                else:
                    return False, None, None
            elif Player.Moderator:
                if DataStore.Get("StaffLogger", "ModeratorCommands") == "true":
                    return True, "ModeratorLog", " typed: /"
                else:
                    return False, None, None
            elif DataStore.Get("StaffLogger", "PlayerCommands") == "true":
                return True, "PlayerLog", " typed: /"
            else:
                return False, None, None
        elif typee == "Chat":
            if Player.Owner:
                if DataStore.Get("StaffLogger", "OwnerChat") == "true":
                    return True, "OwnerLog", " said: "
                else:
                    return False, None, None
            elif Player.Admin:
                if DataStore.Get("StaffLogger", "AdminChat") == "true":
                    return True, "AdminLog", " said: "
                else:
                    return False, None, None
            elif Player.Moderator:
                if DataStore.Get("StaffLogger", "ModeratorChat") == "true":
                    return True, "ModeratorLog", " said: "
                else:
                    return False, None, None
            elif DataStore.Get("StaffLogger", "PlayerChat") == "true":
                return True, "PlayerLog", " said: "
            else:
                return False, None, None
        elif typee == "Loot":
            if Player.Owner:
                if DataStore.Get("StaffLogger", "OwnerLooting") == "true":
                    return True, "OwnerLog", " looted: "
                else:
                    return False, None, None
            elif Player.Admin:
                if DataStore.Get("StaffLogger", "AdminLooting") == "true":
                    return True, "AdminLog", " looted: "
                else:
                    return False, None, None
            elif Player.Moderator:
                if DataStore.Get("StaffLogger", "ModeratorLooting") == "true":
                    return True, "ModeratorLog", " looted: "
                else:
                    return False, None, None
            elif DataStore.Get("StaffLogger", "PlayerLooting") == "true":
                return True, "PlayerLog", " looted: "
            else:
                return False, None, None
