__title__ = 'TroubleinTerroristTown'
__author__ = 'Jakkee & DreTaX'
__about__ = 'GameMode: Trouble in Terrorist Town'
__version__ = '1.3Beta'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp")
import CommunityEntity
import Network
import Pluton
import sys
import re
path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")
try:
    import random
    import datetime
    import time
except ImportError:
    raise ImportError("Trouble in Terrorist Town: Can not find folder Lib [Pluton\Python\Lib] *DOWNLOAD: http://forum.pluton-team.org/resources/ironpython-extra-libs.43/*")
try:
    import json
except ImportError:
    raise ImportError("Trouble in Terrorist Town: Can not find folder JSON in Libs folder [Pluton\Python\JSON] *DOWNLOAD: http://forum.pluton-team.org/resources/microjson.54/*")

rgbstringtemplate = re.compile(r'#[a-fA-F0-9]{6}$')
KillData = {}
PlayerLocData = {}
PluginSettings = {}
# TODO: HUD ui may need to be moved, Playing with graphics.hud false currently (Just testing, Might keep)
hud = [
    {
        "name": "hudui",
        "parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.3",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.005",
                "anchormax": "0.2 0.085"
            }
        ]
    },
    {
        "parent": "hudui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "[COLOR]",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.01 0.55",
                "anchormax": "0.75 0.95"
            }
        ]
    },
    {
        "parent": "hudui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[INFOBOX]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.01 0.55",
                "anchormax": "0.75 0.95"
            }
        ]
    },
    {
        "parent": "hudui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[TIME]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.755 0.55",
                "anchormax": "0.995 0.95"
            }
        ]
    }
]
health = [
    {
        "name": "healthui",
        "parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.3 0.3 0.3 0.2",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.007 0.010",
                "anchormax": "0.195 0.040"
            }
        ]
    },
    {
        "parent": "healthui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.08 0.8 0.12 0.5",
            },
            {
                "type": "RectTransform",
                "anchormin": "0 0",
                "anchormax": "[INTHEALTH] 1"
            }
        ]
    },
    {
        "parent": "healthui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[HEALTH]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0 0",
                "anchormax": "1 1"
            }
        ]
    }
]
broadcast = [
    {
        "name": "broadcastui",
        "parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.5",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.205 0.005",
                "anchormax": "0.795 0.04"
            }
        ]
    },
    {
        "parent": "broadcastui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[TEXT]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0 0",
                "anchormax": "1 1"
            }
        ]
    }
]
winner = [
    {
        "name": "winnerui",
        "parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.4",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.25 0.95",
                "anchormax": "0.75 0.995"
            }
        ]
    },
    {
        "parent": "winnerui",
        "components":
        [
            {
                "type": "UnityEngine.UI.Text",
                "text": "[TEXT]",
                "fontSize": 20,
                "align": "MiddleCenter",
            },
            {
                "type": "RectTransform",
                "anchormin": "0 0",
                "anchormax": "1 1"
            }
        ]
    }
]

# End of UI's


class TroubleinTerroristTown:

    amountofterrorists = 0
    amountofinnocents = 0
    countdown = 0
    matchlength = 0
    prepperiod = 0
    resettime = 0
    GameTick = 0

    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "SystemName", "Trouble in Terrorist Town")
            ini.AddSetting("Settings", ";SystemName", "Plugins chat name")
            ini.AddSetting("Settings", "Preparation Period", "30")
            ini.AddSetting("Settings", ";Preparation Period",
                           "After x seconds check player count (Starts game if it meets min players)")
            ini.AddSetting("Settings", "CountDown", "20")
            ini.AddSetting("Settings", ";CountDown", "For how many seconds should we do a countdown for?")
            ini.AddSetting("Settings", "FreezePlayerLocTimer", "600")
            ini.AddSetting("Settings", ";FreezePlayerLocTimer", "How many milliseconds should we reset the players location while doing a countdown. 300 for less than 10 players, 500 for 10-20 players & 1000 for 50+ players.")
            ini.AddSetting("Settings", "GameTick", "1000")
            ini.AddSetting("Settings", ";GameTick", "1000 = 1 second. This is how many Millisec's the game timer runs at (Only change if you know what you're doing)")
            ini.AddSetting("Settings", "Min Players", "6")
            ini.AddSetting("Settings", ";Min Players", "How many players need to be online for the game to start")
            ini.AddSetting("Settings", "KillMistakeAmount", "0")
            ini.AddSetting("Settings", ";KillMistakeAmount", "How many times can an Innocent kill other Innocents before he/she is killed/respawned and force to specate?")
            ini.AddSetting("Settings", "Match length", "300")
            ini.AddSetting("Settings", ";Match length", "How many seconds should a game go for? 300 = 5mins")
            ini.AddSetting("Settings", "ResetTime", "10")
            ini.AddSetting("Settings", ";ResetTime","How many seconds should the game have a cooldown between games (Dead players will still be specating until this is over)")
            ini.AddSetting("Settings", "Leave Messages", "True")
            ini.AddSetting("Settings", ";Leave Message", "Display leave messages if an Innocent/Terrorist left?")
            ini.AddSetting("Settings", "Destroyable Buildings", "False")
            ini.AddSetting("Settings", ";Destroyable Buildings",
                           "Did you create a small island with some objects you don't want destroyed? (Server wide)")
            # ini.AddSetting("Settings", ";Destroyable Deloyables", "False")
            # ini.AddSetting("Settings", "", "")
            ini.AddSetting("Messages", "AwaitingPlayers", "Waiting for players")
            # ini.AddSetting("Messages", "Not Enough Players", "Not enough players to start! Retrying in: %Time% seconds")
            ini.AddSetting("Messages", "CountDown", "Loading game")
            ini.AddSetting("Messages", "Round Over", "Round over")
            ini.AddSetting("Messages", "GameStarted", "Preparation period is now over! Find the Terrorist!")
            ini.AddSetting("Messages", "Winner", "%Winner%'s win!")
            ini.AddSetting("Messages", "Reset", "Resetting game in %Time% seconds...")
            ini.AddSetting("Messages", "GroupReminder", "You have been selected to be: %Group%")
            ini.AddSetting("Messages", "LastLeaveMessage", "The last %Group% alive left the server!")
            ini.AddSetting("Messages", "LeaveMessage", "A(n) %Group% left the server!")
            ini.AddSetting("Messages", "Ran out of time", "The match has ended. [Time limit reached]")
            # ini.AddSetting("Messages", "", "")
            ini.AddSetting("InnocentKit", "Wear0", "Boonie Hat, 1")
            ini.AddSetting("InnocentKit", "Wear1", "Hoodie, 1")
            ini.AddSetting("InnocentKit", "Wear2", "Metal Chest Plate, 1")
            ini.AddSetting("InnocentKit", "Wear3", "Leather Gloves, 1")
            ini.AddSetting("InnocentKit", "Wear4", "Pants, 1")
            ini.AddSetting("InnocentKit", "Wear5", "Boots, 1")
            ini.AddSetting("InnocentKit", "Belt0", "Pump Shotgun, 1")
            ini.AddSetting("InnocentKit", "Belt1", "Custom SMG, 1")
            ini.AddSetting("InnocentKit", "Belt2", "Medical Syringe, 1")
            ini.AddSetting("InnocentKit", "Belt3", "Medical Syringe, 1")
            ini.AddSetting("InnocentKit", "Belt4", "Cooked Wolf Meat, 1")
            ini.AddSetting("InnocentKit", "Belt5", "Machete, 1")
            ini.AddSetting("InnocentKit", "Main0", "12 Gauge Buckshot, 64")
            ini.AddSetting("InnocentKit", "Main1", "12 Gauge Buckshot, 64")
            ini.AddSetting("InnocentKit", "Main2", "Pistol Bullet, 64")
            ini.AddSetting("InnocentKit", "Main3", "Pistol Bullet, 64")
            ini.AddSetting("InnocentKit", "Main4", "Medical Syringe, 1")
            ini.AddSetting("TerroristKit", "Wear0", "Boonie Hat, 1")
            ini.AddSetting("TerroristKit", "Wear1", "Hoodie, 1")
            ini.AddSetting("TerroristKit", "Wear2", "Metal Chest Plate, 1")
            ini.AddSetting("TerroristKit", "Wear3", "Leather Gloves, 1")
            ini.AddSetting("TerroristKit", "Wear4", "Pants, 1")
            ini.AddSetting("TerroristKit", "Wear5", "Boots, 1")
            ini.AddSetting("TerroristKit", "Belt0", "Pump Shotgun, 1")
            ini.AddSetting("TerroristKit", "Belt1", "Custom SMG, 1")
            ini.AddSetting("TerroristKit", "Belt2", "Medical Syringe, 1")
            ini.AddSetting("TerroristKit", "Belt3", "Medical Syringe, 1")
            ini.AddSetting("TerroristKit", "Belt4", "Cooked Wolf Meat, 1")
            ini.AddSetting("TerroristKit", "Belt5", "Bone Knife, 1")
            ini.AddSetting("TerroristKit", "Main0", "12 Gauge Buckshot, 64")
            ini.AddSetting("TerroristKit", "Main1", "12 Gauge Buckshot, 64")
            ini.AddSetting("TerroristKit", "Main2", "Pistol Bullet, 64")
            ini.AddSetting("TerroristKit", "Main3", "Pistol Bullet, 64")
            ini.AddSetting("TerroristKit", "Main4", "Medical Syringe, 1")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        PluginSettings.clear()
        DataStore.Flush("TTT")
        DataStore.Flush("InnocentKit")
        DataStore.Flush("TerroristKit")
        for slot in ini.EnumSection("InnocentKit"):
            DataStore.Add("InnocentKit", slot, ini.GetSetting("InnocentKit", slot))
        for slot in ini.EnumSection("TerroristKit"):
            DataStore.Add("TerroristKit", slot, ini.GetSetting("TerroristKit", slot))
        PluginSettings["SystemName"] = ini.GetSetting("Settings", "SystemName")
        PluginSettings["PrepPeriodTime"] = self.Tryint(ini.GetSetting("Settings", "Preparation Period")) * 1000
        PluginSettings["FreezerTimer"] = self.Tryint(ini.GetSetting("Settings", "FreezePlayerLocTimer"))
        PluginSettings["MinPlayers"] = self.Tryint(ini.GetSetting("Settings", "Min Players"))
        PluginSettings["DestroyableBuilding"] = ini.GetBoolSetting("Settings", "Destroyable Buildings")
        PluginSettings["CountDown"] = self.Tryint(ini.GetSetting("Settings", "CountDown"))
        PluginSettings["KillAmount"] = self.Tryint(ini.GetSetting("Settings", "KillMistakeAmount"))
        PluginSettings["MatchLength"] = self.Tryint(ini.GetSetting("Settings", "Match length"))
        PluginSettings["ResetTime"] = self.Tryint(ini.GetSetting("Settings", "ResetTime"))
        PluginSettings["LeaveMessage"] = ini.GetBoolSetting("Settings", "Leave Messages")
        PluginSettings["GameTick"] = self.Tryint(ini.GetSetting("Settings", "GameTick"))
        PluginSettings["MSGAwaitingPlayers"] = self.ColorizeMessage(ini.GetSetting("Messages", "AwaitingPlayers"))
        # PluginSettings["MSGNotEnoughPlayers"] = self.ColorizeMessage(ini.GetSetting("Messages", "Not Enough Players"))
        PluginSettings["MSGCountDown"] = self.ColorizeMessage(ini.GetSetting("Messages", "CountDown"))
        PluginSettings["MSGGameStarted"] = self.ColorizeMessage(ini.GetSetting("Messages", "GameStarted"))
        PluginSettings["MSGWinner"] = self.ColorizeMessage(ini.GetSetting("Messages", "Winner"))
        PluginSettings["MSGReset"] = self.ColorizeMessage(ini.GetSetting("Messages", "Reset"))
        PluginSettings["MSGReminder"] = self.ColorizeMessage(ini.GetSetting("Messages", "GroupReminder"))
        PluginSettings["MSGLastLeave"] = self.ColorizeMessage(ini.GetSetting("Messages", "LastLeaveMessage"))
        PluginSettings["MSGLeave"] = self.ColorizeMessage(ini.GetSetting("Messages", "LeaveMessage"))
        PluginSettings["MSGOutOfTime"] = self.ColorizeMessage(ini.GetSetting("Messages", "Ran out of time"))
        PluginSettings["MSGRoundOver"] = self.ColorizeMessage(ini.GetSetting("Messages", "Round Over"))
        self.countdown = PluginSettings["CountDown"]
        self.matchlength = PluginSettings["MatchLength"]
        self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
        self.resettime = PluginSettings["ResetTime"]
        self.GameTick = PluginSettings["GameTick"]
        self.clearui()
        self.startgame()

    def ColorizeMessage(self, String):
        s = String
        if "COLOR" in s:
            arr = []
            list = s.split('COLOR')
            for part in list:
                if part.isspace() or not part:
                    continue
                words = part.split(' ')
                for word in words:
                    strip = word.strip(' ')
                    if self.IsRGB(strip):
                        color = part.split(' ', 1)[0]
                        themsg = part.split(' ', 1)[1]
                        colorized = self.ColorText(color, themsg)
                        arr.append(colorized)
                        break
            s = ' '.join(arr)
        return s

    def ColorText(self, color, part):
        return '<color=' + color + '>' + part + '</color>'

    def IsRGB(self, value):
        return bool(rgbstringtemplate.match(value))

    def Tryint(self, Arg):
        try:
            number = int(Arg)
            return number
        except Exception, error:
            Plugin.Log("ErrorLog", "Tryint: " + str(error))
            Util.Log("Trouble in Terrorist Town: Can not convert string to int (String was not a number!) Check Settings.ini")
            return None
        
    def GuiHUDCallback(self, timer):
        if DataStore.Get("TTT", "PrepPeriod"):
            if not DataStore.Get("TTT", "DisableKilling"):
                DataStore.Add("TTT", "DisableKilling", True)
            if self.prepperiod >= 0:
                for Player in Server.ActivePlayers:
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "DestroyUI", "hudui")
                    string = json.encode(hud)
                    jsonUI = json.makepretty(string)
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "AddUI", jsonUI.Replace("[INFOBOX]", PluginSettings["MSGAwaitingPlayers"])
                                                               .Replace("[TIME]", str(time.strftime("%M:%S", time.gmtime(self.prepperiod))))
                                                               .Replace("[COLOR]", "0.5 0.5 0.5 0.4"))
                self.prepperiod -= 1
            elif len(Server.ActivePlayers) >= PluginSettings["MinPlayers"]:
                if len(Server.ActivePlayers) == 0:
                    self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
                    return
                else:
                    for Player in Server.SleepingPlayers:
                        Player.Kill()
                    self.setTerrorist()
                    self.setInnocent()
                    DataStore.Remove("TTT", "PrepPeriod")
                    DataStore.Add("TTT", "On_PlayerWakeUp", True)
                    DataStore.Add("TTT", "CountDownPeriod", True)
                    for Player in Server.ActivePlayers:
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                   "DestroyUI", "hudui")
                        Player.Kill()
                        Player.basePlayer.Respawn()
                        Player.basePlayer.metabolism.calories.value = 1000
                        Player.basePlayer.metabolism.hydration.value = 1000
                        Player.Health = 100
                        PlayerLocData[Player.SteamID] = Player.Location
                        DataStore.Add("TTT", "In-Game:" + Player.SteamID, True)
                        for item in Player.Inventory.AllItems():
                            item._item.RemoveFromContainer()
                        if self.findgroup(Player) == "Terrorist":
                            for slot in DataStore.Keys("TerroristKit"):
                                if slot[:-1] == "Wear":
                                    item = DataStore.Get("TerroristKit", slot).split(",")
                                    Player.Inventory.InnerWear.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                                elif slot[:-1] == "Belt":
                                    item = DataStore.Get("TerroristKit", slot).split(",")
                                    Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                                else:
                                    item = DataStore.Get("TerroristKit", slot).split(",")
                                    Player.Inventory.InnerMain.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                        else:
                            for slot in DataStore.Keys("InnocentKit"):
                                if slot[:-1] == "Wear":
                                    item = DataStore.Get("InnocentKit", slot).split(",")
                                    Player.Inventory.InnerWear.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                                elif slot[:-1] == "Belt":
                                    item = DataStore.Get("InnocentKit", slot).split(",")
                                    Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                                else:
                                    item = DataStore.Get("InnocentKit", slot).split(",")
                                    Player.Inventory.InnerMain.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                    Plugin.CreateTimer("CountDown", 1000).Start()
                    Plugin.CreateTimer("FreezePlayers", PluginSettings["FreezerTimer"]).Start()
            else:
                self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
                return
        elif DataStore.Get("TTT", "CountDownPeriod"):
            if self.countdown >= 0:
                for Player in Server.ActivePlayers:
                    if DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                        if Player.basePlayer.IsSleeping():
                            Player.basePlayer.EndSleeping()
                        else:
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                       "DestroyUI", "hudui")
                            string = json.encode(hud)
                            jsonUI = json.makepretty(string)
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                       "AddUI", jsonUI.Replace("[INFOBOX]", PluginSettings["MSGCountDown"])
                                                                       .Replace("[TIME]", str(time.strftime("%M:%S", time.gmtime(self.countdown))))
                                                                       .Replace("[COLOR]", "0.5 0.5 0.5 0.4"))
                    else:
                        continue
                self.countdown -= 1
            else:
                DataStore.Remove("TTT", "CountDownPeriod")
                for Player in Server.ActivePlayers:

                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                       "DestroyUI", "hudui")
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "DestroyUI", "broadcastui")
                    string = json.encode(broadcast)
                    jsonUI = json.makepretty(string)
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "AddUI", jsonUI
                                                               .Replace("[TEXT]", PluginSettings["MSGReminder"]
                                                                        .Replace("%Group%", self.findgroup(Player))))
                    if Player.basePlayer.IsSleeping():
                        Player.basePlayer.EndSleeping()
                    else:
                        continue
                if Plugin.GetTimer("RemoveBroadcast") is not None:
                    Plugin.GetTimer("RemoveBroadcast").Kill()
                Plugin.CreateTimer("RemoveBroadcast", 10000).Start()
                # Todo: Change Server.Broadcast to broadcast UI
                # Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGGameStarted"])
                Plugin.GetTimer("FreezePlayers").Kill()
                DataStore.Remove("TTT", "DisableKilling")
                DataStore.Add("TTT", "INGAME", True)
        elif DataStore.Get("TTT", "INGAME"):
            if self.matchlength >= 0:
                for Player in Server.ActivePlayers:
                    if DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                        group = self.findgroup(Player)
                        color = "0.08 0.8 0.12 0.5"
                        if group == "Terrorist":
                            color = "1 0.08 0.08 0.5"
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                   "DestroyUI", "hudui")
                        string = json.encode(hud)
                        jsonUI = json.makepretty(string)
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                   "AddUI", jsonUI.Replace("[INFOBOX]", self.findgroup(Player))
                                                                   .Replace("[TIME]", str(time.strftime("%M:%S", time.gmtime(self.matchlength))))
                                                                   .Replace("[COLOR]", color))
                    else:
                        continue
                self.matchlength -= 1
            else:
                if not DataStore.Get("TTT", "RoundOver"):
                    self.clearui()
                    # Todo: Change Server.Broadcast to broadcast UI
                    # Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGOutOfTime"])
                    self.endgame("Terrorist")
                else:
                    for Player in Server.ActivePlayers:
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                   "DestroyUI", "hudui")
                        string = json.encode(hud)
                        jsonUI = json.makepretty(string)
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                                   "AddUI", jsonUI.Replace("[INFOBOX]", PluginSettings["MSGRoundOver"])
                                                                   .Replace("[TIME]", str(time.strftime("%M:%S", time.gmtime(self.resettime))))
                                                                   .Replace("[COLOR]", "0.5 0.5 0.5 0.4"))
                    self.resettime -= 1

    def clearui(self):
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "winnerui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "healthui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "hudui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "healthui")

    def endgame(self, winner):
        DataStore.Add("TTT", "RoundOver", True)
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "winnerui")
            string = json.encode(winner)
            jsonUI = json.makepretty(string)
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "AddUI", jsonUI
                                                       .Replace("[TEXT]", PluginSettings["MSGWinner"].Replace("%Winner%", winner)))
        if Plugin.GetTimer("RemoveBroadcast") is not None:
            Plugin.GetTimer("RemoveBroadcast").Kill()
        Plugin.CreateTimer("RemoveBroadcast", 8000).Start()
        Plugin.CreateTimer("Reset", PluginSettings["ResetTime"] * 1000).Start()

    def ResetCallback(self, timer):
        timer.Kill()
        if Plugin.GetTimer("GuiHUD") is not None:
            Plugin.GetTimer("GuiHUD").Kill()
        DataStore.Remove("TTT", "RoundOver")
        DataStore.Remove("TTT", "On_PlayerWakeUp")
        DataStore.Remove("TTT", "INGAME")
        DataStore.Remove("TTT", "CountDownPeriod")
        DataStore.Remove("TTT", "PrepPeriod")
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "winnerui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "broadcastui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                        "DestroyUI", "hudui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                        "DestroyUI", "healthui")
            DataStore.Remove("TTT", "USER:" + Player.SteamID)
            Player.Kill()
            Player.basePlayer.Respawn()
        KillData.clear()
        PlayerLocData.clear()
        self.countdown = PluginSettings["CountDown"]
        self.matchlength = PluginSettings["MatchLength"]
        self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
        self.resettime = PluginSettings["ResetTime"]
        self.amountofterrorists = 0
        self.amountofinnocents = 0
        self.startgame()

    def startgame(self):
        DataStore.Add("TTT", "PrepPeriod", True)
        for Player in Server.ActivePlayers:
            if Player.basePlayer.IsSpectating():
                Player.basePlayer.StopSpectating()
                Player.basePlayer.Respawn()
        if Plugin.GetTimer("GuiHUD") is None:
            Plugin.CreateTimer("GuiHUD", self.GameTick).Start()
        else:
            Plugin.GetTimer("GuiHUD").Start()

    def FreezePlayersCallback(self, timer):
        for Player in Server.ActivePlayers:
            if Util.GetVectorsDistance(Player.Location, PlayerLocData[Player.SteamID]) >= 1:
                Player.basePlayer.MovePosition(PlayerLocData[Player.SteamID])
                Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "ForcePositionTo",
                                                  PlayerLocData[Player.SteamID])
                Player.basePlayer.TransformChanged()
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                           "DestroyUI", "broadcastui")
                for timer in Plugin.GetParallelTimer("Broadcast"):
                    if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                        timer.Kill()
                string = json.encode(broadcast)
                jsonUI = json.makepretty(string)
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                           "AddUI", jsonUI
                                                           .Replace("[TEXT]", "Wait until the countdown is finished!"))
                data = Plugin.CreateDict()
                data["PlayerID"] = Player.GameID
                Plugin.CreateParallelTimer("Broadcast", 1300, data).Start()

    def On_PlayerWakeUp(self, Player):
        if DataStore.Get("TTT", "On_PlayerWakeUp"):
            if not DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                Player.basePlayer.StartSpectating()
                return
            else:
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                           "DestroyUI", "healthui")
                string = json.encode(health)
                jsonUI = json.makepretty(string)
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI",
                                                           jsonUI.Replace("[HEALTH]", str(round(Player.Health, 0)).split(".")[0])
                                                           .Replace("[INTHEALTH]", str(round(Player.Health, 2)/100)))

    def On_PlayerHealthChange(self, PlayerHealthChangeEvent):
        Player = PlayerHealthChangeEvent
        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                   "DestroyUI", "healthui")
        if DataStore.Get("TTT", "In-Game:" + Player.SteamID):
            string = json.encode(health)
            jsonUI = json.makepretty(string)
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI",
                                                       jsonUI.Replace("[HEALTH]", str(round(Player.Health, 0)).split(".")[0])
                                                       .Replace("[INTHEALTH]", str(round(Player.Health, 2)/100)))
        else:
            return

    def RemoveBroadcastCallback(self, timer):
        timer.Kill()
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                   "DestroyUI", "broadcastui")

    def BroadcastCallback(self, timer):
        timer.Kill()
        data = timer.Args
        playerID = data["PlayerID"]
        Player = Server.Players[playerID]
        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                   "DestroyUI", "broadcastui")

    def PlayerDisconnected(self, Player):
        if not DataStore.Get("TTT", "GAMEOVER"):
            if self.findgroup(Player) == "Terrorist":
                self.amountofterrorists -= 1
                if self.amountofterrorists == 0:
                    if PluginSettings["LeaveMessage"]:
                        Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGLastLeave"]
                                             .Replace("%Group%", self.findgroup(Player)))
                    self.endgame("Innocent")
                else:
                    if PluginSettings["LeaveMessage"]:
                        Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGLeave"]
                                             .Replace("%Group%", self.findgroup(Player)))
            else:
                if self.findgroup(Player) == "Innocent":
                    self.amountofinnocents -= 1
                    if self.amountofinnocents == 0:
                        if PluginSettings["LeaveMessage"]:
                            Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGLastLeave"]
                                                 .Replace("%Group%", self.findgroup(Player)))
                        self.endgame("Terrorist")
                    else:
                        if DataStore.Get("TTT", "LeaveMessage"):
                            Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGLastLeave"]
                                                 .Replace("%Group%", self.findgroup(Player)))
        # DataStore.Remove("TTT", "USER:" + Player.SteamID)
        DataStore.Remove("TTT", "In-Game:" + Player.SteamID)

    def setTerrorist(self):
        #try:
            totalplayers = Server.ActivePlayers
            need = round(len(totalplayers) / 3, 0)
            need = str(need).split(".")[0]
            need = int(need)
            if need == 0:
                need = 1
            maax = need + 1
            self.amountofterrorists = need
            randlist = random.sample(xrange(1, maax), need)
            count = 0
            for Player in totalplayers:
                count += 1
                for x in randlist:
                    if count == x:
                        DataStore.Add("TTT", "USER:" + Player.SteamID, "Terrorist")
                        # Player.MessageFrom("Terrorist", "You have been selected to be a: Terrorist")
                        # Player.MessageFrom("Terrorist", "Kill players without the others knowing it was you!")
                        continue
                else:
                    continue
        #except Exception, error:
            #Server.Broadcast("Error setting terrorists, Reload the server!")
            #Plugin.Log("ErrorLog", "setTerrorist: " + str(error))

    def setInnocent(self):
        for Player in Server.ActivePlayers:
            if self.findgroup(Player) == "Terrorist":
                continue
            else:
                self.amountofinnocents += 1
                DataStore.Add("TTT", "USER:" + Player.SteamID, "Innocent")
                # Player.MessageFrom("Innocent", "You have been selected to be an: Innocent")
                # Player.MessageFrom("Innocent", "Hunt down the Terrorist! If you kill an Innocent you will be killed")
                continue

    def findgroup(self, Player):
        return DataStore.Get("TTT", "USER:" + Player.SteamID)

    def On_CombatEntityHurt(self, CombatEntityHurtEvent):
        if not PluginSettings["DestroyableBuilding"]:
            for x in range(0, len(CombatEntityHurtEvent.DamageAmounts)):
                CombatEntityHurtEvent.DamageAmounts[x] = 0

    def On_PlayerHurt(self, PlayerHurtEvent):
        try:
            if DataStore.Get("TTT", "DisableKilling"):
                for x in range(0, len(PlayerHurtEvent.DamageAmounts)):
                    PlayerHurtEvent.DamageAmounts[x] = 0
            else:
                try:
                    if PlayerHurtEvent.Weapon.Name == "Bone Knife":
                        if PlayerHurtEvent.Attacker.IsPlayer():
                            Attacker = PlayerHurtEvent.Attacker.ToPlayer()
                            if self.findgroup(Attacker) == "Terrorist":
                                for x in range(0, len(PlayerHurtEvent.DamageAmounts)):
                                    PlayerHurtEvent.DamageAmounts[x] = 100
                except:
                    return
                        
        except Exception, error:
            Plugin.Log("ErrorLog", "On_PlayerHurt: " + str(error))
            return

    def On_PlayerDied(self, PlayerDeathEvent):
        # Todo: Display kill feed in top right hand corner, Thats more GarrysMod style
        # Todo: E.G: Attacker Name *Gun symbol* Victim Name
        # Todo: Fully test this hook, Sometimes works.
        #try:
            PlayerDeathEvent.dropLoot = False
            if DataStore.Get("TTT", "INGAME"):
                Victim = PlayerDeathEvent.Victim
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "healthui")
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "hudui")
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "healthui")
                if PlayerDeathEvent.Attacker.IsPlayer():
                    Attacker = PlayerDeathEvent.Attacker.ToPlayer()
                    if self.findgroup(Victim) == "Terrorist":
                        Server.BroadcastFrom(PluginSettings["SystemName"], Attacker.Name
                                             + " has killed a Terrorist [" + Victim.Name + "]")
                        self.amountofterrorists -= 1
                        if self.amountofterrorists == 0:
                            Plugin.GetTimer("GuiHUD").Kill()
                            self.clearui()
                            self.endgame("Innocent")
                        else:
                            Server.BroadcastFrom(PluginSettings["SystemName"], str(self.amountofterrorists)
                                                 + " Terrorist(s) remain!")
                    elif self.findgroup(Victim) == "Innocent":
                        if self.findgroup(Attacker) == "Terrorist":
                            self.amountofinnocents -= 1
                            if not PlayerDeathEvent.Weapon.Name == "Bone Knife":
                                Server.BroadcastFrom(PluginSettings["SystemName"],
                                                     "A Terrorist has killed a player [" + Victim.Name + "]")
                                if self.amountofinnocents == 0:
                                    Plugin.GetTimer("GuiHUD").Kill()
                                    self.clearui()
                                    self.endgame("Terrorist")
                            else:
                                Attacker.MessageFrom(PluginSettings["SystemName"], "That kill was silent!")
                                if self.amountofinnocents == 0:
                                    Plugin.GetTimer("GuiHUD").Kill()
                                    self.clearui()
                                    self.endgame("Terrorist")
                        elif KillData[Attacker.SteamID] >= DataStore.Get("TTT", "KillAmount"):
                            Attacker.Kill()
                            Attacker.basePlayer.Respawn()
                            amount = PluginSettings["KillAmount"]
                            if amount == 0:
                                amount = 1
                            Server.BroadcastFrom(PluginSettings["SystemName"], Attacker.Name + " has killed "
                                                 + str(amount)
                                                 + " Innocent player(s) and has been killed for his actions!")
                        else:
                            KillData[Attacker.SteamID] += 1
                            Server.BroadcastFrom(PluginSettings["SystemName"], Attacker.Name
                                                 + " has killed an Innocent! " + Victim.Name + "]")
                    else:
                        if DataStore.Contains("TTT", "In-Game:" + Victim.SteamID):
                            Plugin.Log("ErrorLog", "On_PlayerDied: " + Victim.Name
                                       + " was not either a Terrorist or an Innocent!")
                else:
                    if self.findgroup(PlayerDeathEvent.Victim) == "Terrorist":
                        Server.BroadcastFrom(PluginSettings["SystemName"], "A Terrorist ["
                                             + PlayerDeathEvent.Victim.Name + "] has been killed by natural forces")
                        self.amountofterrorists -= 1
                        if self.amountofterrorists == 0:
                            Plugin.GetTimer("GuiHUD").Kill()
                            self.clearui()
                            self.endgame("Innocent")
                    else:
                        Server.BroadcastFrom(PluginSettings["SystemName"], "An Innocent ["
                                             + PlayerDeathEvent.Victim.Name + "] has been killed by natural forces")
                        self.amountofinnocents -= 1
                        if self.amountofinnocents == 0:
                            Plugin.GetTimer("GuiHUD").Kill()
                            self.clearui()
                            self.endgame("Terrorist")
                            # TODO: test?
                DataStore.Remove("TTT", "In-Game:" + Victim.SteamID)
        #except Exception, error:
            #Plugin.Log("ErrorLog", "On_PlayerDied: " + str(error))
