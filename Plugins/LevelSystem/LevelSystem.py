__title__ = 'LevelSystem'
__author__ = 'Jakkee'
__about__ = 'Get extra resources'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp-firstpass", "Assembly-CSharp")
import Pluton
import Facepunch
import CommunityEntity
import Network
import sys
import re
path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")
try:
    import json
except ImportError:
    raise ImportError(__title__ + ": Can not find JSON in Libs folder [Pluton\Python\Lib] DOWNLOAD: http://forum.pluton-team.org/resources/microjson.54/")
level = [
    {
        "name": "levelui",
        #"parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.4",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.7 0.5",
                "anchormax": "0.995 0.85"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.4 0.4 0.4 0.3",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.665",
                "anchormax": "0.99 0.995"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[WCStats]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.665",
                "anchormax": "0.99 0.995"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.4 0.4 0.4 0.3",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.33",
                "anchormax": "0.99 0.66"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[MININGStats]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.33",
                "anchormax": "0.99 0.66"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.4 0.4 0.4 0.3",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.005",
                "anchormax": "0.99 0.325"
            }
        ]
    },
    {
        "parent": "levelui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[SKININGStats]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.005",
                "anchormax": "0.99 0.325"
            }
        ]
    },
]
string = json.encode(level)
levels = json.makepretty(string)


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
            if int(ini.GetSetting("Settings", "AutoSave data interval")) >= 0:
                Plugin.CreateTimer("SaveData", int(ini.GetSetting("Settings", "AutoSave data interval")) * 1000).Start()
        except Exception, error:
            Util.Log(__title__ + ": There is an error in your settings file!")
            Util.Log(__title__ + ": " + str(error))
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("levelui"))

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

    def On_PlayerGathering(self, GatherEvent):
        if int(GatherEvent.ResourceDispenser.gatherType) == 0:
            self.amounthandler(GatherEvent.ItemAmount, GatherEvent.Resource, GatherEvent.Gatherer, GatherEvent.Amount, "W", "WEXP")
        elif int(GatherEvent.ResourceDispenser.gatherType) == 1:
            self.amounthandler(GatherEvent.ItemAmount, GatherEvent.Resource, GatherEvent.Gatherer, GatherEvent.Amount, "M", "MEXP")
        elif int(GatherEvent.ResourceDispenser.gatherType) == 2:
            self.amounthandler(GatherEvent.ItemAmount, GatherEvent.Resource, GatherEvent.Gatherer, GatherEvent.Amount, "S", "SEXP")

    def amounthandler(self, itemamount, item, Player, amount, skill, skillexp):
        calc = DataStore.Get("PlayerData", Player.SteamID + skill) * 0.20
        giveamount = amount * calc
        if giveamount >= 1:
            Player.Inventory.Add(itemamount.itemid, giveamount)
        thingy = DataStore.Get("PlayerData", Player.SteamID + skillexp) + int(DataStore.Get("LevelSystem", "EXPHIT"))
        DataStore.Add("PlayerData", Player.SteamID + skillexp, thingy) 
        self.LevelHandler(Player, skill, skillexp)

    def LevelHandler(self, Player, skill, skillexp):
        need = self.expcalc(Player.SteamID, skillexp)
        if not need == 0:
            if DataStore.Get("PlayerData", Player.SteamID + skillexp) >= need:
                exp = DataStore.Get("PlayerData", Player.SteamID + skillexp)
                DataStore.Add("PlayerData", Player.SteamID + skillexp, exp - need)
                level = DataStore.Get("PlayerData", Player.SteamID + skill) + 1
                DataStore.Add("PlayerData", Player.SteamID + skill, level)
                Player.Message("You have gained a new level!")
                self.ShowStats(Player)
            else:
                return
        else:
            return

    def expcalc(self, steamID, skill):
        try:
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
                return "MaxLevel"
        except:
            return 0

    def ShowLevelUICallback(self, timer):
        try:
            timer.Kill()
            data = timer.Args
            playerID = data["PlayerID"]
            Player = Server.Players[playerID]
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("levelui"))
        except:
            pass

    def ShowStats(self, Player):
        for timer in Plugin.GetParallelTimer("ShowLevelUI"):
            if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                timer.Kill()
        data = Plugin.CreateDict()
        data["PlayerID"] = Player.GameID
        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("levelui"))
        wexp = str(self.expcalc(Player.SteamID, "WEXP"))
        if wexp == "MaxLevel":
            WStats = ("Woodcutting Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "W")) + " [Exp: Max Level Reached]")
        else:
            WStats = ("Woodcutting Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "W")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "WEXP")) + "/" + wexp + "]")
        mexp = str(self.expcalc(Player.SteamID, "MEXP"))
        if mexp == "MaxLevel":
            MStats = ("Mining Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "M")) + " [Exp: Max level Reached]")
        else:
            MStats = ("Mining Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "M")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "MEXP")) + "/" + mexp + "]")
        sexp = str(self.expcalc(Player.SteamID, "SEXP"))
        if sexp == "MaxLevel":
            SStats = ("Skinning Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "S")) + " [Exp: Max level Reached]")
        else:
            SStats = ("Skinning Level: " + str(DataStore.Get("PlayerData", Player.SteamID + "S")) + " [Exp: " + str(DataStore.Get("PlayerData", Player.SteamID + "SEXP")) + "/" + sexp + "]")
        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", Facepunch.ObjectList(levels.Replace("[WCStats]", WStats).Replace("[MININGStats]", MStats).Replace("[SKININGStats]", SStats)))
        Plugin.CreateParallelTimer("ShowLevelUI", 10000, data).Start()

    def stats(self, args, Player):
        if len(args) == 0:
            if Player.Owner or Player.Admin or Player.Moderator:
                Player.Message('/level set ["Players Name"] [skill] [Level]')
                Player.Message('/level wipe - Clears all data!')
            self.ShowStats(Player)
        else:
            if Player.Owner or Player.Admin or Player.Moderator:
                if args[0] == "set":
                    if len(args) == 4:
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
                elif args[0] == "wipe":
                    if Plugin.IniExists("PlayerData"):
                        Server.Broadcast("Wiping levels systems data..")
                        try:
                            data = Plugin.GetIni("PlayerData")
                            DataStore.Flush("PlayerData")
                            for offlineplayer in Server.OfflinePlayers.Values:
                                data.DeleteSection(offlineplayer.SteamID)
                            for pl in Server.ActivePlayers:
                                data.DeleteSection(pl.SteamID)
                                DataStore.Add("PlayerData", Player.SteamID + "WEXP", 0)
                                DataStore.Add("PlayerData", Player.SteamID + "SEXP", 0)
                                DataStore.Add("PlayerData", Player.SteamID + "MEXP", 0)
                                DataStore.Add("PlayerData", Player.SteamID + "W", 0)
                                DataStore.Add("PlayerData", Player.SteamID + "M", 0)
                                DataStore.Add("PlayerData", Player.SteamID + "S", 0)
                            data.Save()
                            Server.Broadcast("Completed!")
                        except Exception, error:
                            Player.Message("Failed: " + str(error))
                    else:
                        Player.Message("Nothing to delete!")
                else:
                    Player.Message('/level set ["Players Name"] [skill] [Level]')
                    Player.Message('/level wipe - Clears all data!')
            else:
                Player.Message("You do not have permission to use this command!")         

    def On_PlayerConnected(self, Player):
        data = Plugin.GetIni("PlayerData")
        try:
            if data.ContainsSetting(Player.SteamID, "WoodCutting"):
                self.getstats(Player.SteamID)
            else:
                DataStore.Add("PlayerData", Player.SteamID + "W", 0)
                DataStore.Add("PlayerData", Player.SteamID + "WEXP", 0)
                DataStore.Add("PlayerData", Player.SteamID + "M", 0)
                DataStore.Add("PlayerData", Player.SteamID + "MEXP", 0)
                DataStore.Add("PlayerData", Player.SteamID + "S", 0)
                DataStore.Add("PlayerData", Player.SteamID + "SEXP", 0)
        except:
            DataStore.Add("PlayerData", Player.SteamID + "W", 0)
            DataStore.Add("PlayerData", Player.SteamID + "WEXP", 0)
            DataStore.Add("PlayerData", Player.SteamID + "M", 0)
            DataStore.Add("PlayerData", Player.SteamID + "MEXP", 0)
            DataStore.Add("PlayerData", Player.SteamID + "S", 0)
            DataStore.Add("PlayerData", Player.SteamID + "SEXP", 0)

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
