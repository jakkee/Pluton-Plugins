__title__ = 'LevelSystem'
__author__ = 'Jakkee'
__about__ = 'Get extra resources'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class LevelSystem:
    def On_PluginInit(self):
        Commands.Register("level").setCallback("stats").setDescription("Check your levels").setUsage("/level")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "EXP per hit", "2")
            ini.AddSetting("Settings", "Mining level cap", "50")
            ini.AddSetting("Settings", "WoodCutting level cap", "50")
            ini.AddSetting("Settings", "Skinning level cap", "50")
            ini.AddSetting("Settings", "AutoSave data interval", "120")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        try:
            DataStore.Add("LevelSystem", "EXPHIT", int(ini.GetSetting("Settings", "EXP per hit")))
            DataStore.Add("LevelSystem", "M", int(ini.GetSetting("Settings", "Mining level cap")))
            DataStore.Add("LevelSystem", "W", int(ini.GetSetting("Settings", "WoodCutting level cap")))
            DataStore.Add("LevelSystem", "S", int(ini.GetSetting("Settings", "Skinning level cap")))
            if not ini.GetSetting("Settings", "AutoSave data interval") == "-1":
                Plugin.CreateTimer("SaveData", int(ini.GetSetting("Settings", "AutoSave data interval")) * 1000)
        except:
            Util.Log("----------------------------------------------------------")
            Util.Log("LevelSystem: Failed to convert String to a number!")
            Util.Log("LevelSystem: String was not a number, Check your settings!")
            Util.Log("----------------------------------------------------------")

    def SaveDataCallback(self, timer):
        try:
            Util.Log("LevelSystem: Saving player data...")
            for player in Server.ActivePlayers:
                self.dumpstats(player.SteamID)
            for player in Server.OfflinePlayers.Values:
                self.dumpstats(player.SteamID)
            Util.Log("LevelSystem: Saved player data!")
        except:
            Util.Log("LevelSystem: Error in AutoSaving players data!")

    def On_Gather(self, GatherEvent):
        Server.Broadcast(str(int(GatherEvent.ResourceDispenser.gatherType)))
        if int(GatherEvent.ResourceDispenser.gatherType) == 0:
            self.amounthandler(GatherEvent.Gatherer, GatherEvent.Amount, "W", "WEXP")
        elif int(GatherEvent.ResourceDispenser.gatherType) == 1:
            self.mining(GatherEvent.Gatherer, GatherEvent.Amount, "M", "MEXP")
        elif int(GatherEvent.ResourceDispenser.gatherType) == 2:
            self.skinning(GatherEvent.Gatherer, GatherEvent.Amount, "S", "SEXP")

    def amounthandler(self, Player, amount, skill, skillexp):
        calc = DataStore.Get("PlayerData", Player.SteamID + skill) * 0.20
        if not calc == 0:
            Player.Inventory.Add(GatherEvent.Resource.Name, amount * calc)
        thingy = DataStore.Get("PlayerData", Player.SteamID + skillexp) + int(DataStore.Add("LevelSystem", "EXPHIT"))
        DataStore.Add("PlayerData", Player.SteamID + skillexp, thingy) 
        self.LevelHandler(Player, skill, skillexp)

    def LevelHandler(self, Player, skill, skillexp):
        need = self.expcalc(Player.SteamID, skillexp)
        if not need == 0:
            if DataStore.Get("PlayerData", Player.SteamID + skillexp) >= need:
                num = DataStore.Get("PlayerData", Player.SteamID + skillexp)
                DataStore.Add("PlayerData", Player.SteamID + skillexp, num - need)
                thing = DataStore.Get("PlayerData", Player.SteamID + skill) + 1
                DataStore.Add("PlayerData", Player.SteamID + skill, thing)
                Player.Message("You have gained a level!")
            else:
                return
        else:
            return

    def expcalc(self, steamID, skill):
        level = DataStore.Get("PlayerData", steamID + skill[:-3])
        level = int(level)
        maxlevel = DataStore.Get("LevelSystem", skill[:-3])
        maxlevel = int(maxlevel) - 1
        if level <= maxlevel:
            calc = level * 1.8
            if calc == 0:
                calc = 1
            need = 15 * calc
            return need
        else:
            return 0
    
    def stats(self, args, Player):
        if len(args) == 0:
            wexp = str(self.expcalc(Player.SteamID, "WEXP"))
            if wexp == "0":
                Player.MessageFrom("WoodCutting", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "W")) + " [Exp: Max Level Reached]")
            else:
                Player.MessageFrom("WoodCutting", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "W")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "WEXP")) + "/" + wexp + "]")
            mexp = str(self.expcalc(Player.SteamID, "MEXP"))
            if mexp == "0":
                Player.MessageFrom("Mining", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "M")) + " [Exp: Max level Reached]")
            else:
                Player.MessageFrom("Mining", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "M")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "MEXP")) + "/" + mexp + "]")
            sexp = str(self.expcalc(Player.SteamID, "SEXP"))
            if sexp == "0":
                Player.MessageFrom("Skinning", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "S")) + " [Exp: Max level Reached]")
            else:
                Player.MessageFrom("Skinning", "Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "S")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "SEXP")) + "/" + sexp + "]")
            if Player.Owner or Player.Admin or Player.Moderator:
                Player.Message("--------------------------------------------------")
                Player.Message('Usage: /level set ["Players Name"] [skill] [Level]')
                Player.Message('Example: /level set "360 Pro Noob" m 33')
                Player.Message('Skills are: W=WoodCutting, M=Mining & S=Skinning')
                Player.Message("--------------------------------------------------")
        else:
            if Player.Owner or Player.Admin or Player.Moderator:
                if len(args) == 4:
                    if args[0] == "set":
                        name = self.CheckV(Player, args[1])
                        if name is not None:
                            skill = args[2].upper()
                            level = int(args[3])
                            DataStore.Add("PlayerData", Player.SteamID + skill, level)
                            Player.Message("Changed " + name.Name + "'s level to " + args[3])
                        else:
                            return
                    else:
                        Player.Message('Usage: /level set ["Players Name"] [skill] [Level]')
                        Player.Message('Example: /level set "360 Pro Noob" m 33')
                        Player.Message('Skills are: W=WoodCutting, M=Mining & S=Skinning')
                else:
                    Player.Message('Usage: /level set ["Players Name"] [skill] [Level]')
                    Player.Message('Example: /level set "360 Pro Noob" m 33')
                    Player.Message('Skills are: W=WoodCutting, M=Mining & S=Skinning')
            else:
                Player.Message("You do not have permission to use this command!")         

    def On_PlayerConnected(self, Player):
        data = Plugin.GetIni("PlayerData")
        if data.ContainsSetting(Player.SteamID, "WoodCutting"):
            self.getstats(Player.SteamID)
        else:
            DataStore.Add("PlayerData", Player.SteamID + "W", int(0))
            DataStore.Add("PlayerData", Player.SteamID + "WEXP", int(0))
            DataStore.Add("PlayerData", Player.SteamID + "M", int(0))
            DataStore.Add("PlayerData", Player.SteamID + "MEXP", int(0))
            DataStore.Add("PlayerData", Player.SteamID + "S", int(0))
            DataStore.Add("PlayerData", Player.SteamID + "SEXP", int(0))

    def On_PlayerDisconnected(self, Player):
        self.dumpstats(Player.SteamID)

    def dumpstats(self, steamid):
        if not Plugin.IniExists("PlayerData"):
            Plugin.CreateIni("PlayerData")
        data = Plugin.GetIni("PlayerData")
        data.AddSetting(steamid, "WoodCutting", str(DataStore.Get("PlayerData", steamid + "W")))
        data.AddSetting(steamid, "WoodCuttingEXP", str(DataStore.Get("PlayerData", steamid + "WEXP")))
        data.AddSetting(steamid, "Mining", str(DataStore.Get("PlayerData", steamid + "M")))
        data.AddSetting(steamid, "MiningEXP", str(DataStore.Get("PlayerData", steamid + "MEXP")))
        data.AddSetting(steamid, "Skinning", str(DataStore.Get("PlayerData", steamid + "S")))
        data.AddSetting(steamid, "SkinningEXP", str(DataStore.Get("PlayerData", steamid + "SEXP")))
        data.Save()

    def getstats(self, steamid):
        data = Plugin.GetIni("PlayerData")
        DataStore.Add("PlayerData", steamid + "W", int(data.GetSetting(steamid, "WoodCutting")))
        DataStore.Add("PlayerData", steamid + "WEXP", int(data.GetSetting(steamid, "WoodCuttingEXP")))
        DataStore.Add("PlayerData", steamid + "M", int(data.GetSetting(steamid, "Mining")))
        DataStore.Add("PlayerData", steamid + "MEXP", int(data.GetSetting(steamid, "MiningEXP")))
        DataStore.Add("PlayerData", steamid + "S", int(data.GetSetting(steamid, "Skinning")))
        DataStore.Add("PlayerData", steamid + "SEXP", int(data.GetSetting(steamid, "SkinningEXP")))

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        Mode: 3 (Searches Online/Offline players)
        V5.0
    """

    def GetPlayerName(self, name):
        Name = name.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == Name:
                return pl
        for pl in Server.OfflinePlayers.Values:
            if pl.Name.lower() == Name:
                return pl
        return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
            for offlineplayer in Server.OfflinePlayers.Values:
                for namePart in args:
                    if namePart.lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if str(args).lower() in pl.Name.lower():
                    p = pl
                    count += 1
            for offlineplayer in Server.OfflinePlayers.Values:
                if str(args).lower() in offlineplayer.Name.lower():
                    p = offlineplayer
                    count += 1
        if count == 0:
            Player.Message("Couldn't find player: " + args + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " player with similar name. Use more correct name!")
            return None
