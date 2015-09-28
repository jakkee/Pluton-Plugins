__title__ = 'TroubleinTerroristTown'
__author__ = 'Jakkee & DreTaX'
__about__ = 'GameMode: Trouble in Terrorist Town'
__version__ = '1.2Beta'

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
terroristdata = {}
PlayerLocData = {}
PluginSettings = {}


class TroubleinTerroristTown:

    amountofterrorists = 0
    amountofinnocents = 0
    countdown = 0
    matchlength = 0
    prepperiod = 0
    resettime = 0

    def On_PluginInit(self):
        terroristdata[0] = 1
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
            ini.AddSetting("Settings", "Min Players", "6")
            ini.AddSetting("Settings", ";Min Players", "How many players need to be online for the game to start")
            ini.AddSetting("Settings", "KillMistakeAmount", "0")
            ini.AddSetting("Settings", ";KillMistakeAmount", "How many times can an Innocent kill other Innocents before he/she is killed/respawned and force to specate?")
            ini.AddSetting("Settings", "Match length", "480")
            ini.AddSetting("Settings", ";Match length", "How many seconds should a game go for? 480 = 5mins")
            ini.AddSetting("Settings", "ResetTime", "10")
            ini.AddSetting("Settings", ";ResetTime","How many seconds should the game have a cooldown between games (Dead players will still be specating until this is over)")
            ini.AddSetting("Settings", "Leave Messages", "True")
            ini.AddSetting("Settings", ";Leave Message", "Display leave messages if an Innocent/Terrorist left?")
            ini.AddSetting("Settings", "Destroyable Buildings", "False")
            ini.AddSetting("Settings", ";Destroyable Buildings",
                           "Did you create a small island with some objects you don't want destroyed? (Server wide)")
            # ini.AddSetting("Settings", ";Destroyable Deloyables", "False")
            # ini.AddSetting("Settings", "", "")
            ini.AddSetting("Messages", "AwaitingPlayers", "Awaiting players")
            # ini.AddSetting("Messages", "Not Enough Players", "Not enough players to start! Retrying in: %Time% seconds")
            ini.AddSetting("Messages", "CountDown", "Starting in..")
            ini.AddSetting("Messages", "Round Over", "Round over")
            ini.AddSetting("Messages", "GameStarted", "Preparation period is now over! Find the Terrorist!")
            ini.AddSetting("Messages", "Winner", "%Winner%'s win!")
            ini.AddSetting("Messages", "Reset", "Resetting game in %Time% seconds...")
            ini.AddSetting("Messages", "GroupReminder", "Remember you're a(n): %Group%")
            ini.AddSetting("Messages", "LastLeaveMessage", "The last %Group% alive left the server!")
            ini.AddSetting("Messages", "LeaveMessage", "A(n) %Group% left the server!")
            ini.AddSetting("Messages", "Ran out of time", "The match has ended. [Time limit reached]")
            # ini.AddSetting("Messages", "", "")
            ini.Save()
        # Todo: Storing values in the class should be faster than DS
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("TTT")
        PluginSettings.clear()
        PluginSettings["SystemName"] = ini.GetSetting("Settings", "SystemName")
        PluginSettings["PrepPeriodTime"] = self.Tryint(ini.GetSetting("Settings", "Preparation Period")) * 1000
        PluginSettings["FreezerTimer"] = self.Tryint(ini.GetSetting("Settings", "FreezePlayerLocTimer"))
        PluginSettings["MinPlayers"] = self.Tryint(ini.GetSetting("Settings", "Min Players"))
        PluginSettings["DestroyableBuilding"] = ini.GetBoolSetting("Settings", "Destroyable Buildings")
        PluginSettings["CountDown"] = self.Tryint(ini.GetSetting("Settings", "CountDown"))
        PluginSettings["KillAmount"] = self.Tryint(ini.GetSetting("Settings", "KillMistakeAmount"))
        PluginSettings["MatchLength"] = self.Tryint(ini.GetSetting("Settings", "Match length"))
        PluginSettings["ResetTime"] = self.Tryint(ini.GetSetting("Settings", "ResetTime")) * 1000
        PluginSettings["LeaveMessage"] = ini.GetBoolSetting("Settings", "Leave Messages")
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
        self.resettime = PluginSettings["ResetTime"] / 1000
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
        #time.strftime("%M:%S", time.gmtime(Seconds))
        if DataStore.Get("TTT", "PrepPeriod"):
            if not DataStore.Get("TTT", "DisableKilling"):
                DataStore.Add("TTT", "DisableKilling", True)
            if self.prepperiod > 0:
                PrepPeriodui = [
                    {
                        "name": "PrepPeriodui",
                        "parent": "Overlay",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Image",
                                "color": "0.1 0.1 0.1 1",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.821 0.15",
                                "anchormax": "0.973 0.2"
                            }
                        ]
                    },
                    {
                        "parent": "PrepPeriodui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": PluginSettings["MSGAwaitingPlayers"],
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0 0",
                                "anchormax": "0.75 1"
                            }
                        ]
                    },
                    {
                        "parent": "PrepPeriodui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": str(time.strftime("%M:%S", time.gmtime(self.prepperiod))),
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.7 0",
                                "anchormax": "1 1"
                            }
                        ]
                    }
                ]
                stringit = json.encode(PrepPeriodui)
                PrepPeriodUI = json.makepretty(stringit)
                for Player in Server.ActivePlayers:
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "DestroyUI", "PrepPeriodui")
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "AddUI", PrepPeriodUI)
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
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection),
                                                                   None, "DestroyUI", "PrepPeriodui")
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
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Boonie Hat"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Leather Gloves"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Hoodie"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Pants"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Boots"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Custom SMG"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Pump Shotgun"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Medical Syringe"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Medical Syringe"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Cooked Wolf Meat"), 20)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Bone Knife"), 1)
                            Player.Inventory.InnerMain.AddItem(Find.ItemDefinition("Pistol Bullet"), 500)
                            Player.Inventory.InnerMain.AddItem(Find.ItemDefinition("12 Gauge Buckshot"), 64)
                        else:
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Boonie Hat"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Leather Gloves"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Hoodie"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Pants"), 1)
                            Player.Inventory.InnerWear.AddItem(Find.ItemDefinition("Boots"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Custom SMG"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Pump Shotgun"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Medical Syringe"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Medical Syringe"), 1)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Cooked Wolf Meat"), 20)
                            Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition("Machete"), 1)
                            Player.Inventory.InnerMain.AddItem(Find.ItemDefinition("Pistol Bullet"), 500)
                            Player.Inventory.InnerMain.AddItem(Find.ItemDefinition("12 Gauge Buckshot"), 64)
                            # Player.Inventory.Add()
                    Plugin.CreateTimer("CountDown", 1000).Start()
                    Plugin.CreateTimer("FreezePlayers", PluginSettings["FreezerTimer"]).Start()
            else:
                self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
                return
        elif DataStore.Get("TTT", "CountDownPeriod"):
            if self.countdown > 0:
                CountDownui = [
                    {
                        "name": "CountDownui",
                        "parent": "Overlay",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Image",
                                "color": "0.1 0.1 0.1 1",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.821 0.15",
                                "anchormax": "0.973 0.2"
                            }
                        ]
                    },
                    {
                        "parent": "CountDownui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": PluginSettings["MSGCountDown"],
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0 0",
                                "anchormax": "0.65 1"
                            }
                        ]
                    },
                    {
                        "parent": "CountDownui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": str(time.strftime("%M:%S", time.gmtime(self.countdown))),
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.7 0",
                                "anchormax": "1 1"
                            }
                        ]
                    }
                ]
                stringit1 = json.encode(CountDownui)
                CountDown = json.makepretty(stringit1)
                for Player in Server.ActivePlayers:
                    if DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                        if Player.basePlayer.IsSleeping():
                            Player.basePlayer.EndSleeping()
                        else:
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", "CountDownui")
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", CountDown)
                    else:
                        continue
                self.countdown -= 1
            else:
                DataStore.Remove("TTT", "CountDownPeriod")
                for Player in Server.ActivePlayers:
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                               "DestroyUI", "CountDownui")
                    Player.MessageFrom(PluginSettings["SystemName"], PluginSettings["MSGReminder"]
                                       .Replace("%Group%", self.findgroup(Player)))
                    if Player.basePlayer.IsSleeping():
                        Player.basePlayer.EndSleeping()
                    else:
                        continue
                Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGGameStarted"])
                Plugin.GetTimer("FreezePlayers").Kill()
                DataStore.Remove("TTT", "DisableKilling")
                DataStore.Add("TTT", "INGAME", True)
        elif DataStore.Get("TTT", "INGAME"):
            if self.matchlength > 0:
                Terroristui = [
                    {
                        "name": "Terroristui",
                        "parent": "Overlay",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Image",
                                "color": "0.1 0.1 0.1 1",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.821 0.15",
                                "anchormax": "0.973 0.2"
                            }
                        ]
                    },
                    {
                        "parent": "Terroristui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": "Terrorist",
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0 0",
                                "anchormax": "0.75 1"
                            }
                        ]
                    },
                    {
                        "parent": "Terroristui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": str(time.strftime("%M:%S", time.gmtime(self.matchlength))),
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.7 0",
                                "anchormax": "1 1"
                            }
                        ]
                    }
                ]
                stringit = json.encode(Terroristui)
                TerroristUI = json.makepretty(stringit)
                Innocentui = [
                    {
                        "name": "Innocentui",
                        "parent": "Overlay",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Image",
                                "color": "0.1 0.1 0.1 1",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.821 0.15",
                                "anchormax": "0.973 0.2"
                            }
                        ]
                    },
                    {
                        "parent": "Innocentui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": "Innocent",
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0 0",
                                "anchormax": "0.75 1"
                            }
                        ]
                    },
                    {
                        "parent": "Innocentui",
                        "components":
                        [
                            {
                                "type": "UnityEngine.UI.Text",
                                "text": str(time.strftime("%M:%S", time.gmtime(self.matchlength))),
                                "fontSize": 20,
                                "align": "MiddleCenter",
                            },
                            {
                                "type": "RectTransform",
                                "anchormin": "0.7 0",
                                "anchormax": "1 1"
                            }
                        ]
                    }
                ]
                stringit1 = json.encode(Innocentui)
                InnocentUI = json.makepretty(stringit1)
                for Player in Server.ActivePlayers:
                    if DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection),
                                                                   None, "DestroyUI", "Innocentui")
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection),
                                                                   None, "DestroyUI", "Terroristui")
                        if self.findgroup(Player) == "Terrorist":
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", TerroristUI)
                        else:
                            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", InnocentUI)
                    else:
                        continue
                self.matchlength -= 1
            else:
                if not DataStore.Get("TTT", "RoundOver"):
                    self.clearui()
                    Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGOutOfTime"])
                    self.endgame("Terrorist")
                else:
                    RoundOverui = [
                        {
                            "name": "RoundOverui",
                            "parent": "Overlay",
                            "components":
                            [
                                {
                                    "type": "UnityEngine.UI.Image",
                                    "color": "0.1 0.1 0.1 1",
                                },
                                {
                                    "type": "RectTransform",
                                    "anchormin": "0.821 0.15",
                                    "anchormax": "0.973 0.2"
                                }
                            ]
                        },
                        {
                            "parent": "RoundOverui",
                            "components":
                            [
                                {
                                    "type": "UnityEngine.UI.Text",
                                    "text": PluginSettings["MSGRoundOver"],
                                    "fontSize": 20,
                                    "align": "MiddleCenter",
                                },
                                {
                                    "type": "RectTransform",
                                    "anchormin": "0 0",
                                    "anchormax": "0.75 1"
                                }
                            ]
                        },
                        {
                            "parent": "RoundOverui",
                            "components":
                            [
                                {
                                    "type": "UnityEngine.UI.Text",
                                    "text": str(time.strftime("%M:%S", time.gmtime(self.resettime))),
                                    "fontSize": 20,
                                    "align": "MiddleCenter",
                                },
                                {
                                    "type": "RectTransform",
                                    "anchormin": "0.7 0",
                                    "anchormax": "1 1"
                                }
                            ]
                        }
                    ]
                    stringit = json.encode(RoundOverui)
                    RoundOverUI = json.makepretty(stringit)
                    for Player in Server.ActivePlayers:
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection),
                                                                   None, "DestroyUI", "RoundOverui")
                        CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection),
                                                                   None, "AddUI", RoundOverUI)
                    self.resettime -= 1

    def clearui(self):
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "Winnerui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "RoundOverui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "PrepPeriodui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "CountDownui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "Innocentui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "Terroristui")

    def endgame(self, winner):
        DataStore.Add("TTT", "RoundOver", True)
        # TODO: UI with winner (Maybe Player name?)
        # Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGWinner"].Replace("%Winner%", winner))
        Winnerui = [
            {
                "name": "Winnerui",
                "parent": "Overlay",
                "components":
                [
                    {
                        "type": "UnityEngine.UI.Image",
                        "color": "0.1 0.1 0.1 1",
                    },
                    {
                        "type": "RectTransform",
                        "anchormin": "0.4 0.94",
                        "anchormax": "0.6 0.98"
                    }
                ]
            },
            {
                "parent": "Winnerui",
                "components":
                [
                    {
                        "type": "UnityEngine.UI.Text",
                        "text": PluginSettings["MSGWinner"].Replace("%Winner%", winner),
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
        stringit = json.encode(Winnerui)
        WinnerUI = json.makepretty(stringit)
        for Player in Server.ActivePlayers:
            #CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", "Winnerui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "AddUI", WinnerUI)
        Server.BroadcastFrom(PluginSettings["SystemName"], PluginSettings["MSGReset"]
                             .Replace("%Time%", str(PluginSettings["ResetTime"] / 1000)))
        Plugin.CreateTimer("Reset", PluginSettings["ResetTime"]).Start()

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
                                                       "DestroyUI", "Winnerui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "RoundOverui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "PrepPeriodui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "CountDownui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "Innocentui")
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                       "DestroyUI", "Terroristui")
            DataStore.Remove("TTT", "USER:" + Player.SteamID)
            Player.Kill()
            Player.basePlayer.Respawn()
        KillData.clear()
        terroristdata.clear()
        PlayerLocData.clear()
        self.countdown = PluginSettings["CountDown"]
        self.matchlength = PluginSettings["MatchLength"]
        self.prepperiod = PluginSettings["PrepPeriodTime"] / 1000
        self.resettime = PluginSettings["ResetTime"] / 1000
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
            Plugin.CreateTimer("GuiHUD", 1000).Start()
        else:
            Plugin.GetTimer("GuiHUD").Start()
        # Display GUI with Prep time instead of broadcast
        #Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGPrepPeriod")
                             #.Replace("%Time%", str(time.strftime("%M:%S", time.gmtime(DataStore.Get("TTT", "PrepPeriodTime") / 1000)))))
        #Plugin.CreateTimer("PrepPeriod", int(DataStore.Get("TTT", "PrepPeriodTime"))).Start()

    def FreezePlayersCallback(self, timer):
        for Player in Server.ActivePlayers:
            if Util.GetVectorsDistance(Player.Location, PlayerLocData[Player.SteamID]) >= 1:
                Player.basePlayer.MovePosition(PlayerLocData[Player.SteamID])
                Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "ForcePositionTo",
                                                  PlayerLocData[Player.SteamID])
                Player.basePlayer.TransformChanged()
                Player.MessageFrom(PluginSettings["SystemName"], "Wait until the countdown is finished!")

    def On_PlayerWakeUp(self, Player):
        if DataStore.Get("TTT", "On_PlayerWakeUp"):
            if not DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                Player.basePlayer.StartSpectating()        

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
        try:
            totalplayers = Server.ActivePlayers
            need = round(len(totalplayers) / 3, 0)
            need = str(need).split(".")[0]
            need = int(need)
            if need == 0:
                need = 1
            maax = need + 1
            self.amountofterrorists = need
            randlist = random.sample(xrange(0, maax), need)
            count = 0
            for Player in totalplayers:
                count += 1
                for x in randlist:
                    if count == x:
                        DataStore.Add("TTT", "USER:" + Player.SteamID, "Terrorist")
                        Player.MessageFrom("Terrorist", "You have been selected to be a: Terrorist")
                        Player.MessageFrom("Terrorist", "Kill players without the others knowing it was you!")
                        continue
                else:
                    continue
        except Exception, error:
            Server.Broadcast("Error setting terrorists, Reload the server!")
            Plugin.Log("ErrorLog", "setTerrorist: " + str(error))

    def setInnocent(self):
        for Player in Server.ActivePlayers:
            if self.findgroup(Player) == "Terrorist":
                continue
            else:
                self.amountofinnocents += 1
                DataStore.Add("TTT", "USER:" + Player.SteamID, "Innocent")
                Player.MessageFrom("Innocent", "You have been selected to be an: Innocent")
                Player.MessageFrom("Innocent", "Hunt down the Terrorist! If you kill an Innocent you will be killed")
                continue

    def findgroup(self, Player):
        return DataStore.Get("TTT", "USER:" + Player.SteamID)

    def On_CombatEntityHurt(self, CombatEntityHurtEvent):
        if not PluginSettings["DestroyableBuilding"]:
            for x in range(0, len(CombatEntityHurtEvent.DamageAmounts)):
                CombatEntityHurtEvent.DamageAmounts[x] = 0

    def On_PlayerHurt(self, PlayerHurtEvent):
        try:
            if PluginSettings["DisableKilling"]:
                for x in range(0, len(PlayerHurtEvent.DamageAmounts)):
                    PlayerHurtEvent.DamageAmounts[x] = 0
            else:
                if PlayerHurtEvent.Weapon.Name == "Bone Knife":
                    if PlayerHurtEvent.Attacker.IsPlayer():
                        Attacker = PlayerHurtEvent.Attacker.ToPlayer()
                        if self.findgroup(Attacker) == "Terrorist":
                            for x in range(0, len(PlayerHurtEvent.DamageAmounts)):
                                PlayerHurtEvent.DamageAmounts[x] = 100
                        
        except Exception, error:
            Plugin.Log("ErrorLog", "On_PlayerHurt: " + str(error))
            return

    def On_PlayerDied(self, PlayerDeathEvent):
        # Display kill feed in top right hand corner, Thats more GarrysMod style
        # E.G: Attacker Name *Gun symbol* Victim Name
        try:
            PlayerDeathEvent.dropLoot = False
            if DataStore.Get("TTT", "INGAME"):
                Victim = PlayerDeathEvent.Victim
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "PrepPeriodui")
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "CountDownui")
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "Innocentui")
                CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Victim.basePlayer.net.connection), None,
                                                           "DestroyUI", "Terroristui")
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
        except Exception, error:
            Plugin.Log("ErrorLog", "On_PlayerDied: " + str(error))
