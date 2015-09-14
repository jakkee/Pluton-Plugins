__title__ = 'Warps'
__author__ = 'Jakkee'
__about__ = 'Add warps and teleport to them'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import System

 
class Warps:
    def On_PluginInit(self):
        Commands.Register("warp").setCallback("warp").setDescription("Teleport to a warp").setUsage("/warp go [Warp Name]")
        if not Plugin.IniExists("WarpData"):
            Plugin.CreateIni("WarpData")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "Chat Name", "Warp System")
            ini.AddSetting("Settings", "CoolDown", "120")
            ini.AddSetting("Settings", "Admin CoolDown", "1")
            ini.AddSetting("Settings", "Teleport Delay", "15")
            ini.AddSetting("Settings", "Admin Teleport Delay", "1")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("Warps")
        DataStore.Flush("WarpsData")
        DataStore.Add("Warps", "Cooldown", self.Tryint(ini.GetSetting("Settings", "CoolDown")) * 1000)
        DataStore.Add("Warps", "AdminCooldown", self.Tryint(ini.GetSetting("Settings", "Admin CoolDown")) * 1000)
        DataStore.Add("Warps", "Delay", self.Tryint(ini.GetSetting("Settings", "Teleport Delay")) * 1000)
        DataStore.Add("Warps", "AdminDelay", self.Tryint(ini.GetSetting("Settings", "Admin Teleport Delay")) * 1000)
        DataStore.Add("Warps", "Chatname", ini.GetSetting("Settings", "Chat Name"))
        data = Plugin.GetIni("WarpData")
        for key in data.EnumSection("WarpData"):
            DataStore.Add("WarpsData", key, data.GetSetting("WarpData", key))

    def Tryint(self, Arg):
        try:
            arg = int(Arg)
            return arg
        except:
            return None

    def TeleportDelayCallback(self, timer):
        timer.Kill()
        Data = timer.Args
        Player = Data["Player"]
        locname = Data["LocationName"]
        loc = Data["Location"]
        Player.Teleport(float(loc[0]), float(loc[1]), float(loc[2]))
        Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "You have warped to: " + locname)
        DataStore.Add("Warps", Player.SteamID, System.Environment.TickCount)
        
    def warp(self, args, Player):
        if len(args) == 0:
            if Player.Owner or Player.Admin or Player.Moderator:
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp add <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp del <name>")
            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp go <name>")
            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp list")
        elif len(args) == 1:
            if args[0] == "list":
                if DataStore.Count("WarpsData") > 0:
                    count = 1
                    for key in DataStore.Keys("WarpsData"):
                        Player.MessageFrom(DataStore.Get("Warps", "Chatname"), str(count) + ") " + key)
                        count += 1
                else:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "This server has no warps setup yet!")
            else:
                if Player.Owner or Player.Admin or Player.Moderator:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp add <name>")
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp del <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp go <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp list")
        elif len(args) == 2:
            if args[0] == "add":
                if Player.Owner or Player.Admin or Player.Moderator:
                    if len(args[1]) > 1:
                        if str(DataStore.Get("WarpsData", args[1])) == "None":
                            data = Plugin.GetIni("WarpData")
                            data.AddSetting("WarpData", args[1], str(Player.Location))
                            data.Save()
                            DataStore.Add("WarpsData", args[1], str(Player.Location))
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Created a warp called " + args[1])
                        else:
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Warp " + args[1] + " already exists!")
                    else:
                        Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "The location name can not be one character long!")
                else:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "You are not allowed to use this command!")
            elif args[0] == "del":
                if Player.Owner or Player.Admin or Player.Moderator:
                    if len(args[1]) > 1:
                        if not str(DataStore.Get("WarpsData", args[1])) == "None":
                            data = Plugin.GetIni("WarpData")
                            data.DeleteSetting("WarpData", args[1])
                            data.Save()
                            DataStore.Remove("WarpsData", args[1])
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Deleted a warp called " + args[1])
                        else:
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Warp " + args[1] + " does not exist!")
                    else:
                        Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "The location name can not be one character long!")
                else:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "You are not allowed to use this command!")
            elif args[0] == "go":
                if DataStore.Get("WarpsData", args[1]) is not None:
                    if Player.Owner or Player.Admin or Player.Moderator:
                        waittime = DataStore.Get("Warps", "AdminCooldown")
                        time = DataStore.Get("Warps", Player.SteamID)
                        try:
                            time = int(time)
                        except:
                            time = 0
                        calc = System.Environment.TickCount - time
                        if calc >= waittime:
                            delay = DataStore.Get("Warps", "AdminDelay")
                            Data = Plugin.CreateDict()
                            Data["Player"] = Player
                            Data["LocationName"] = args[1]
                            location = DataStore.Get("WarpsData", args[1])[1:-1].replace(",", "").split(" ")
                            Data["Location"] = location
                            Plugin.CreateParallelTimer("TeleportDelay", int(delay), Data).Start()
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Teleporting in " + str(delay / 1000) + " seconds.")
                        else:
                            workingout = round((waittime / 1000) - float(calc / 1000), 3)
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), str(workingout) + " seconds remaining before you can use this.")
                    else:
                        waittime = DataStore.Get("Warps", "Cooldown")
                        time = DataStore.Get("Warps", Player.SteamID)
                        try:
                            time = int(time)
                        except:
                            time = 0
                        calc = System.Environment.TickCount - time
                        if calc >= waittime:
                            delay = DataStore.Get("Warps", "Delay")
                            Data = Plugin.CreateDict()
                            Data["Player"] = Player
                            Data["LocationName"] = args[1]
                            location = DataStore.Get("WarpsData", args[1])[1:-1].replace(",", "").split(" ")
                            Data["Location"] = location
                            Plugin.CreateParallelTimer("TeleportDelay", int(delay), Data).Start()
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Teleporting in " + str(delay / 1000) + " seconds.")
                        else:
                            workingout = round((waittime / 1000) - float(calc / 1000), 3)
                            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), str(workingout) + " seconds remaining before you can use this.")
                else:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "Warp " + args[1] + " does not exist!")
            elif args[0] == "list":
                if DataStore.Count("WarpsData") > 0:
                    count = 1
                    for key in DataStore.Keys("WarpsData"):
                        Player.MessageFrom(DataStore.Get("Warps", "Chatname"), str(count) + ") " + key)
                        count += 1
                else:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "This server has no warps setup yet!")

            else:
                if Player.Owner or Player.Admin or Player.Moderator:
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp add <name>")
                    Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp del <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp go <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp list")
        else:
            if Player.Owner or Player.Admin or Player.Moderator:
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp add <name>")
                Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp del <name>")
            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp go <name>")
            Player.MessageFrom(DataStore.Get("Warps", "Chatname"), "/warp list")
