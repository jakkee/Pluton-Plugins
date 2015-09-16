__title__ = 'TroubleinTerroristTown'
__author__ = 'Jakkee'
__about__ = 'GameMode: Trouble in Terrorist Town'
__version__ = '1.0.1Beta'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
import sys
path = Util.GetPublicFolder()
sys.path.append(path + "\\Addons\\Lib\\")
# Todo: Rename to Python, since the documentation uses that folder everywhere?
# Normally use Python Folder, But Addons folder sounds more appropriate
try:
    import random
    import time
except ImportError:
    Util.Log("Trouble in Terrorist Town: Import Error, Download extra Python Libs from: http://forum.pluton-team.org/resources/ironpython-extra-libs.43/")
    raise ImportError("Trouble in Terrorist Town: Can not find folder Lib [Pluton\Addons\Lib]")

KillData = {}
terroristdata = {}
PlayerLocData = {}


class TroubleinTerroristTown:

    amountofterrorists = 0
    amountofinnocents = 0
    countdown = 0

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
            ini.AddSetting("Settings", ";ResetTime", "How many seconds should the game have a cooldown between games (Dead players will still be specating until this is over)")
            ini.AddSetting("Settings", "Leave Messages", "True")
            ini.AddSetting("Settings", ";Leave Message", "Display leave messages if an Innocent/Terrorist left?")
            ini.AddSetting("Settings", "Destroyable Buildings", "False")
            ini.AddSetting("Settings", ";Destroyable Buildings", "Did you create a small island with some objects you don't want destroyed? (Server wide)")
            #ini.AddSetting("Settings", ";Destroyable Deloyables", "False")
            #ini.AddSetting("Settings", "", "")
            ini.AddSetting("Messages", "PrepPeriod", "Game will start countdown in %Time% seconds")
            ini.AddSetting("Messages", "Not Enough Players", "Not enough players to start! Retrying in: %Time% seconds")
            ini.AddSetting("Messages", "CountDown", "Game starting in: %Time% seconds")
            ini.AddSetting("Messages", "GameStarted", "Preparation period is now over! Find the Terrorist!")
            ini.AddSetting("Messages", "Winner", "%Winner%'s wins!")
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
        DataStore.Add("TTT", "SystemName", ini.GetSetting("Settings", "SystemName"))
        DataStore.Add("TTT", "PrepPeriodTime", self.Tryint(ini.GetSetting("Settings", "Preparation Period")) * 1000)
        DataStore.Add("TTT", "FreezerTimer", self.Tryint(ini.GetSetting("Settings", "FreezePlayerLocTimer")))
        DataStore.Add("TTT", "MinPlayers", self.Tryint(ini.GetSetting("Settings", "Min Players")))
        DataStore.Add("TTT", "DestroyableBuilding", ini.GetBoolSetting("Settings", "Destroyable Buildings"))
        # DataStore.Add("TTT", "DestroyableDeloy", ini.GetBoolSetting("Settings", "Destroyable Deloyables"))
        DataStore.Add("TTT", "CoolDown", self.Tryint(ini.GetSetting("Settings", "CountDown")))
        DataStore.Add("TTT", "KillAmount", self.Tryint(ini.GetSetting("Settings", "KillMistakeAmount")))
        DataStore.Add("TTT", "MatchLength", self.Tryint(ini.GetSetting("Settings", "Match length")) * 1000)
        DataStore.Add("TTT", "ResetMatch", self.Tryint(ini.GetSetting("Settings", "ResetTime")) * 1000)
        DataStore.Add("TTT", "LeaveMessage", ini.GetBoolSetting("Settings", "Leave Messages"))
        # DataStore.Add("TTT", "", ini.GetSetting("Settings", ""))
        DataStore.Add("TTT", "MSGPrepPeriod", ini.GetSetting("Messages", "PrepPeriod"))
        DataStore.Add("TTT", "MSGNotEnoughPlayers", ini.GetSetting("Messages", "Not Enough Players"))
        DataStore.Add("TTT", "MSGCountDown", ini.GetSetting("Messages", "CountDown"))
        DataStore.Add("TTT", "MSGGameStarted", ini.GetSetting("Messages", "GameStarted"))
        DataStore.Add("TTT", "MSGWinner", ini.GetSetting("Messages", "Winner"))
        DataStore.Add("TTT", "MSGReset", ini.GetSetting("Messages", "Reset"))
        DataStore.Add("TTT", "MSGReminder", ini.GetSetting("Messages", "GroupReminder"))
        DataStore.Add("TTT", "MSGLastLeave", ini.GetSetting("Messages", "LastLeaveMessage"))
        DataStore.Add("TTT", "MSGLeave", ini.GetSetting("Messages", "LeaveMessage"))
        DataStore.Add("TTT", "MSGOutOfTime", ini.GetSetting("Messages", "Ran out of time"))
        # DataStore.Add("TTT", "MSG", ini.GetSetting("Messages", ""))
        self.countdown = DataStore.Get("TTT", "CoolDown")
        if Lib:
            self.startgame()
        else:
            Util.Log("Trouble in Terrorist Town: Import Error, Download extra Python Libs from: http://forum.pluton-team.org/resources/ironpython-extra-libs.43/")
            Util.Log("Trouble in Terrorist Town: Can not find folder Lib [Pluton\Addons\Lib]")

    def Tryint(self, Arg):
        try:
            number = int(Arg)
            return number
        except Exception, error:
            Plugin.Log("ErrorLog", "Tryint: " + str(error))
            return None

    def endgame(self, winner):
        DataStore.Add("TTT", "PrepPeriod", True)
        DataStore.Add("TTT", "GAMEOVER", True)
        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGWinner").Replace("%Winner%", winner))
        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGReset").Replace("%Time%", str(DataStore.Get("TTT", "ResetMatch") / 1000)))
        Plugin.CreateTimer("Reset", int(DataStore.Get("TTT", "ResetMatch"))).Start()

    def ResetCallback(self, timer):
        timer.Kill()
        Plugin.GetTimer("MatchLength").Kill()
        DataStore.Remove("TTT", "On_PlayerWakeUp")
        for Player in Server.ActivePlayers:
            DataStore.Remove("TTT", "USER:" + Player.SteamID)
            Player.basePlayer.Die()
            Player.basePlayer.Respawn()
        KillData.clear()
        terroristdata.clear()
        PlayerLocData.clear()
        self.countdown = DataStore.Get("TTT", "CoolDown")
        self.amountofterrorists = 0
        self.amountofinnocents = 0
        self.startgame()

    def startgame(self):
        DataStore.Add("TTT", "PrepPeriod", True)
        # Display GUI with Prep time instead of broadcast
        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGPrepPeriod")
                             .Replace("%Time%", str(DataStore.Get("TTT", "PrepPeriodTime") / 1000)))
        Plugin.CreateTimer("PrepPeriod", int(DataStore.Get("TTT", "PrepPeriodTime"))).Start()

    def PrepPeriodCallback(self, timer):
        for Player in Server.ActivePlayers:
            if Player.basePlayer.IsSleeping():
                Player.basePlayer.EndSleeping()
            else:
                continue
        if len(Server.ActivePlayers) >= DataStore.Get("TTT", "MinPlayers"):
            if len(Server.ActivePlayers) == 0:
                Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGNotEnoughPlayers")
                                     .Replace("%Time%", str(DataStore.Get("TTT", "PrepPeriodTime") / 1000)))
            else:
                timer.Kill()
                for Player in Server.SleepingPlayers:
                    Player.basePlayer.Die()
                self.setTerrorist()
                self.setInnocent()
                DataStore.Add("TTT", "On_PlayerWakeUp", True)
                for Player in Server.ActivePlayers:
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
                Plugin.CreateTimer("FreezePlayers", 600).Start()
        else:
            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGNotEnoughPlayers")
                                 .Replace("%Time%", str(DataStore.Get("TTT", "PrepPeriodTime") / 1000)))

    def FreezePlayersCallback(self, timer):
        for Player in Server.ActivePlayers:
            # if Util.GetVectorsDistance(Player.Location, self.PlayerLocData[Player.SteamID]) < 1.5:
            Player.basePlayer.MovePosition(PlayerLocData[Player.SteamID])
            Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "ForcePositionTo", PlayerLocData[Player.SteamID])
            Player.basePlayer.TransformChanged()

    def On_PlayerWakeUp(self, Player):
        if DataStore.Get("TTT", "On_PlayerWakeUp"):
            if not DataStore.Get("TTT", "In-Game:" + Player.SteamID):
                Player.basePlayer.StartSpectating()

    def CountDownCallback(self, timer):
        if self.countdown > 0:
            # Gui here to stop the fucking chat spam
            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGCountDown")
                                 .Replace("%Time%", str(self.countdown)))
            self.countdown -= 1
        else:
            timer.Kill()
            for Player in Server.ActivePlayers:
                if Player.basePlayer.IsSleeping():
                    Player.basePlayer.EndSleeping()
                else:
                    continue
            for Player in Server.ActivePlayers:
                Player.basePlayer.StopSpectating()
                Player.MessageFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGReminder")
                                   .Replace("%Group%", self.findgroup(Player)))
            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGGameStarted"))
            Plugin.GetTimer("FreezePlayers").Kill()
            DataStore.Add("TTT", "PrepPeriod", False)
            Plugin.CreateTimer("MatchLength", int(DataStore.Get("TTT", "MatchLength"))).Start()

    def MatchLengthCallback(self, timer):
        timer.Kill()
        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGOutOfTime"))
        self.endgame("Terrorist")

    def PlayerDisconnected(self, Player):
        if not DataStore.Get("TTT", "GAMEOVER"):
            if self.findgroup(Player) == "Terrorist":
                self.amountofterrorists -= 1
                if self.amountofterrorists == 0:
                    if DataStore.Get("TTT", "LeaveMessage"):
                        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGLastLeave")
                                             .Replace("%Group%", self.findgroup(Player)))
                    self.endgame("Innocent")
                else:
                    if DataStore.Get("TTT", "LeaveMessage"):
                        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGLeave")
                                             .Replace("%Group%", self.findgroup(Player)))
            else:
                if self.findgroup(Player) == "Innocent":
                    self.amountofinnocents -= 1
                    if self.amountofinnocents == 0:
                        if DataStore.Get("TTT", "LeaveMessage"):
                            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"),
                                                 DataStore.Get("TTT", "MSGLastLeave")
                                                 .Replace("%Group%", self.findgroup(Player)))
                        self.endgame("Terrorist")
                    else:
                        if DataStore.Get("TTT", "LeaveMessage"):
                            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), DataStore.Get("TTT", "MSGLeave")
                                                 .Replace("%Group%", self.findgroup(Player)))
        DataStore.Remove("TTT", "USER:" + Player.SteamID)
        DataStore.Remove("TTT", "In-Game:" + Player.SteamID)

    def setTerrorist(self):
        try:
            totalplayers = Server.ActivePlayers
            self.amountofterrorists = round(len(totalplayers) / 3, 0)
            need = round(len(totalplayers) / 3, 0)
            need = str(need).split(".")[0]
            Util.Log(need)
            need = int(need)
            if need == 0:
                self.amountofterrorists = 1
                need = 1
            maax = len(totalplayers) + 1
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
        if not DataStore.Get("TTT", "DestroyableBuilding"):
            for x in range(0, len(CombatEntityHurtEvent.DamageAmounts)):
                CombatEntityHurtEvent.DamageAmounts[x] = 0

    def On_PlayerHurt(self, PlayerHurtEvent):
        try:
            if DataStore.Get("TTT", "PrepPeriod"):
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
            if not DataStore.Get("TTT", "PrepPeriod"):
                Victim = PlayerDeathEvent.Victim
                if PlayerDeathEvent.Attacker.IsPlayer():
                    Attacker = PlayerDeathEvent.Attacker.ToPlayer()
                    if self.findgroup(Victim) == "Terrorist":
                        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), Attacker.Name
                                             + " has killed a Terrorist [" + Victim.Name + "]")
                        self.amountofterrorists -= 1
                        if self.amountofterrorists == 0:
                            self.endgame("Innocent")
                        else:
                            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), str(self.amountofterrorists)
                                                 + " Terrorist(s) remain!")
                    elif self.findgroup(Victim) == "Innocent":
                        if self.findgroup(Attacker) == "Terrorist":
                            self.amountofinnocents -= 1
                            if not PlayerDeathEvent.Weapon.Name == "Bone Knife":
                                Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"),
                                                     "A Terrorist has killed a player [" + Victim.Name + "]")
                                if self.amountofinnocents == 0:
                                    self.endgame("Terrorist")
                            else:
                                Attacker.MessageFrom(DataStore.Get("TTT", "SystemName"), "That kill was silent!")
                                if self.amountofinnocents == 0:
                                    self.endgame("Terrorist")
                        elif KillData[Attacker.SteamID] >= DataStore.Get("TTT", "KillAmount"):
                            Attacker.Kill()
                            Attacker.basePlayer.Respawn()
                            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), Attacker.Name
                                                 + " has killed " + str(DataStore.Get("TTT", "KillAmount"))
                                                 + " Innocent player(s) and has been killed for his actions!")
                        else:
                            KillData[Attacker.SteamID] += 1
                            Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), Attacker.Name
                                                 + " has killed an Innocent! " + Victim.Name + "]")
                    else:
                        if DataStore.Contains("TTT", "In-Game:" + Victim.SteamID):
                            Plugin.Log("ErrorLog", "On_PlayerDied: " + Victim.Name
                                       + " was not either a Terrorist or an Innocent!")
                else:
                    if self.findgroup(PlayerDeathEvent.Victim) == "Terrorist":
                        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), "A Terrorist ["
                                             + PlayerDeathEvent.Victim.Name + "] has been killed by natural forces")
                        self.amountofterrorists -= 1
                        if self.amountofterrorists == 0:
                            self.endgame("Innocent")
                    else:
                        Server.BroadcastFrom(DataStore.Get("TTT", "SystemName"), "An Innocent ["
                                             + PlayerDeathEvent.Victim.Name + "] has been killed by natural forces")
                        self.amountofinnocents -= 1
                        if self.amountofinnocents == 0:
                            self.endgame("Terrorist")
                DataStore.Remove("TTT", "In-Game:" + Victim.SteamID)
        except Exception, error:
            Plugin.Log("ErrorLog", "On_PlayerDied: " + str(error))
