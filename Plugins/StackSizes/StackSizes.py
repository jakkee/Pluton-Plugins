__title__ = 'StackSizes'
__author__ = 'Jakkee'
__version__ = '1.0.5'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp")
import ItemDefinition
import ItemManager
import Pluton


class StackSizes:
    def On_ServerInit(self):
        if not Plugin.IniExists("ItemsList"):
            Plugin.CreateIni("ItemsList")
            ini = Plugin.GetIni("ItemsList")
            items = ItemManager.GetItemDefinitions()
            for item in items:
                ini.AddSetting("StackSizes", item.shortname, str(item.stackable))
                ini.Save()
        ini = Plugin.GetIni("ItemsList")
        for item in ItemManager.GetItemDefinitions():
            if ini.GetSetting("StackSizes", item.shortname) == "" or None:
                ini.AddSetting("StackSizes", item.shortname, str(item.stackable))
                ini.Save()
        self.Set_StackSizes() 

    def On_Command(self, CommandEvent):
        cmd = CommandEvent.cmd
        Player = CommandEvent.User
        args = CommandEvent.args
        if cmd == "stacksizes":
            if Player.Owner or Player.Admin:
                if len(args) == 1:
                    if args == "reload":
                        self.Set_StackSizes()
                        Player.Message("StackSizes have been updated!")
                    else:
                        Player.Message("Usage: /stacksizes reload")
                else:
                    Player.Message("Usage: /stacksizes reload")
            else:
                Player.Message("You are not allow to use this command!")

    def On_ServerConsole(self, ServerConsoleEvent):
        if ServerConsoleEvent.cmd == "stacksizes":
            if len(ServerConsoleEvent.Args) == 1:
                for x in ServerConsoleEvent.Args:
                    if x == "reload":
                        self.Set_StackSizes()
                        Util.Log("StackSizes have been updated!")
                    else:
                        Util.Log("Usage: stacksizes reload")
                    return
            else:
                Util.Log("Usage: stacksizes reload")

    def Set_StackSizes(self):
        ini = Plugin.GetIni("ItemsList")
        for key in ini.EnumSection("StackSizes"):
            if ItemManager.FindItemDefinition(key) == None:
                Util.Log("Could not set stack size for: " + key)
                continue
            ItemManager.FindItemDefinition(key).stackable = int(ini.GetSetting("StackSizes", key))
