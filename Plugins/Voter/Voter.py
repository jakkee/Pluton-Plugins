__title__ = 'Voter'
__author__ = 'Jakkee'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import System
import Pluton


class Voter:

    target = None
    targetname = None
    targetip = None
    targetid = None

    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Day/Night", "Min players online", "5")
            ini.AddSetting("Day/Night", "Percentage Needed", "60%")
            ini.AddSetting("Day/Night", "Cooldown in seconds", "60")
            ini.AddSetting("Day/Night", "Voting length in seconds", "60")
            ini.AddSetting("Day/Night", "Time to change to", "6")
            ini.AddSetting("Day/Night", "Can use command during day?", "false")
            ini.AddSetting("Day/Night", "Players can use?", "true")
            ini.AddSetting("PlayerBan", "Min players online", "5")
            ini.AddSetting("PlayerBan", "Percentage Needed", "75%")
            ini.AddSetting("PlayerBan", "Cooldown in seconds", "60")
            ini.AddSetting("PlayerBan", "Voting length in seconds", "60")
            ini.AddSetting("PlayerBan", "Players can use?", "true")
            ini.AddSetting("PlayerKick", "Min players online", "5")
            ini.AddSetting("PlayerKick", "Percentage Needed", "75%")
            ini.AddSetting("PlayerKick", "Cooldown in seconds", "60")
            ini.AddSetting("PlayerKick", "Voting length in seconds", "60")
            ini.AddSetting("PlayerKick", "Players can use?", "true")
            ini.AddSetting("AirDrop", "Min players online", "5")
            ini.AddSetting("AirDrop", "Percentage Needed", "75%")
            ini.AddSetting("AirDrop", "Cooldown in seconds", "960")
            ini.AddSetting("AirDrop", "Voting length in seconds", "60")
            ini.AddSetting("AirDrop", "Players can use?", "true")
            ini.Save()
        if DataStore.Get("Vote", "type") is not None:
            Server.Broadcast("Server has reloaded which has resulted in stopping the vote")
            Server.Broadcast("Please do not complain to the server staff!")
            self.removetarget()
        DataStore.Flush("VoteNO")
        DataStore.Flush("VoteYES")
        DataStore.Flush("Vote")
        self.killtimer("VotingTimer")
        ini = Plugin.GetIni("Settings")
#Day/Night can use command during day
        DataStore.Add("Vote", "D/N.CanUse", ini.GetSetting("Day/Night", "Can use command during day?"))
#Day/Night change time
        i = self.cn(ini.GetSetting("Day/Night", "Time to change to"))
        if i is not None:
            DataStore.Add("Vote", "D/N.WorldTime", i)
        else:
            DataStore.Add("Vote", "D/N.WorldTime", 6)
#Players can use?
        DataStore.Add("Vote", "D/N.PCU", ini.GetSetting("Day/Night", "Players can use?"))
        DataStore.Add("Vote", "PB.PCU", ini.GetSetting("PlayerBan", "Players can use?"))
        DataStore.Add("Vote", "PK.PCU", ini.GetSetting("PlayerKick", "Players can use?"))
        DataStore.Add("Vote", "AD.PCU", ini.GetSetting("AirDrop", "Players can use?"))
#Voting Length
        i = self.cn(ini.GetSetting("Day/Night", "Voting length in seconds"))
        if i is not None:
            DataStore.Add("Vote", "D/N.VoteLength", i * 1000)
        else:
            DataStore.Add("Vote", "D/N.VoteLength", 60000)
        i = self.cn(ini.GetSetting("PlayerBan", "Voting length in seconds"))
        if i is not None:
            DataStore.Add("Vote", "PB.VoteLength", i * 1000)
        else:
            DataStore.Add("Vote", "PB.VoteLength", 60000)
        i = self.cn(ini.GetSetting("PlayerKick", "Voting length in seconds"))
        if i is not None:
            DataStore.Add("Vote", "PK.VoteLength", i * 1000)
        else:
            DataStore.Add("Vote", "PK.VoteLength", 60000)
        i = self.cn(ini.GetSetting("AirDrop", "Voting length in seconds"))
        if i is not None:
            DataStore.Add("Vote", "AD.VoteLength", i * 1000)
        else:
            DataStore.Add("Vote", "AD.VoteLength", 60000)
#Cooldowns
        i = self.cn(ini.GetSetting("Day/Night", "Cooldown in seconds"))
        if i is not None:
            DataStore.Add("Vote", "D/N.Cooldown", i * 1000)
        else:
            DataStore.Add("Vote", "D/N.Cooldown", 60000)
        i = self.cn(ini.GetSetting("PlayerBan", "Cooldown in seconds"))
        if i is not None:
            DataStore.Add("Vote", "PB.Cooldown", i * 1000)
        else:
            DataStore.Add("Vote", "PB.Cooldown", 60000)
        i = self.cn(ini.GetSetting("PlayerKick", "Cooldown in seconds"))
        if i is not None:
            DataStore.Add("Vote", "PK.Cooldown", i * 1000)
        else:
            DataStore.Add("Vote", "PK.Cooldown", 60000)
        i = self.cn(ini.GetSetting("AirDrop", "Cooldown in seconds"))
        if i is not None:
            DataStore.Add("Vote", "AD.Cooldown", i * 1000)
        else:
            DataStore.Add("Vote", "AD.Cooldown", 960000)
#Percentages needed
        i = self.cn(ini.GetSetting("Day/Night", "Percentage Needed").Replace("%", ""))
        if i is not None:
            DataStore.Add("Vote", "D/N.Min", i)
        else:
            DataStore.Add("Vote", "D/N.Min", 50)
        i = self.cn(ini.GetSetting("PlayerBan", "Percentage Needed").Replace("%", ""))
        if i is not None:
            DataStore.Add("Vote", "PB.Min", i)
        else:
            DataStore.Add("Vote", "PB.Min", 50)
        i = self.cn(ini.GetSetting("PlayerKick", "Percentage Needed").Replace("%", ""))
        if i is not None:
            DataStore.Add("Vote", "PK.Min", i)
        else:
            DataStore.Add("Vote", "PK.Min", 50)
        i = self.cn(ini.GetSetting("AirDrop", "Percentage Needed").Replace("%", ""))
        if i is not None:
            DataStore.Add("Vote", "AD.Min", i)
        else:
            DataStore.Add("Vote", "AD.Min", 50)
#Min players online
        i = self.cn(ini.GetSetting("Day/Night", "Min players online"))
        if i is not None:
            DataStore.Add("Vote", "D/N.MPlayers", i)
        else:
            DataStore.Add("Vote", "D/N.MPlayers", 5)
        i = self.cn(ini.GetSetting("PlayerBan", "Min players online"))
        if i is not None:
            DataStore.Add("Vote", "PB.MPlayers", i)
        else:
            DataStore.Add("Vote", "PB.MPlayers", 5)
        i = self.cn(ini.GetSetting("PlayerKick", "Min players online"))
        if i is not None:
            DataStore.Add("Vote", "PK.MPlayers", i)
        else:
            DataStore.Add("Vote", "PK.MPlayers", 5)
        i = self.cn(ini.GetSetting("AirDrop", "Min players online"))
        if i is not None:
            DataStore.Add("Vote", "AD.MPlayers", i)
        else:
            DataStore.Add("Vote", "AD.MPlayers", 5)

    def removevotes(self):
        try:
            #Might throw an error if a player leaves the server while removing votes, I don't think it would but you can never be sure
            DataStore.Flush("VoteYES")
            DataStore.Flush("VoteNO")
        except:
            pass

    def killtimer(self, name):
        timer = Plugin.GetTimer(name)
        if timer is None:
            return
        timer.Stop()
        Plugin.Timers.Remove(name)

    def cn(self, arg):
        try:
            i = int(arg)
            return i
        except:
            return None

    def removetarget(self):
            self.target = None
            self.targetname = None
            self.targetid = None
            self.targetip = None

    def logban(self, reason):
        try:
            target.Ban(reason)
            self.removetarget()
        except:
            pass

    def On_PlayerDisconnected(self, Player):
        try:
            if DataStore.Get("VoteYES", Player.SteamID) is not None:
                DataStore.Remove("VoteYES", Player.SteamID)
            elif DataStore.Get("VoteNO", Player.SteamID) is not None:
                DataStore.Remove("VoteNO", Player.SteamID)
        except:
            pass

#VoteTimer
    def VoteTimerCallback(self, TimedEvent):
        self.killtimer("VoteTimer")
        total = DataStore.Count("VoteYES") + DataStore.Count("VoteNO")
        try:
            pyes = round((DataStore.Count("VoteYES") / total) * 100, 2)
        except:
            pyes = 0
        try:
            pno = round((DataStore.Count("VoteNO") / total) * 100, 2)
        except:
            pno = 0
        ttype = DataStore.Get("Vote", "type")
        ttype = ttype.split(':')
        if ttype == "D/N":
            min = DataStore.Get("Vote", "D/N.Min")
            if pyes > min:
                World.Time = DataStore.Get("Vote", "D/N.WorldTime", 6)
                Server.Broadcast("The results are in and the servers time has been changed to Day!")
            else:
                Server.Broadcast("The results are in and the servers time has not been changed!")
            Server.Broadcast(str(pyes) + "% voted for Day")
            Server.Broadcast(str(pno) + "% voted for Night")
            DataStore.Add("Vote", "D/N.SysTick", System.Environment.TickCount)
        elif ttype == "PB":
            min = DataStore.Get("Vote", "PB.Min")
            if pyes >= min:
                Server.Broadcast("The results are in and " + self.targetname + " has been banned from the server!")
                Server.Broadcast(str(pyes) + "% voted for Yes")
                Server.Broadcast(str(pno) + "% voted for No")
                self.logban(str(pyes) + "% voted for yes")
            else:
                Server.Broadcast("The results are in and " + self.targetname + " has not been banned from the server!")
                Server.Broadcast(str(pyes) + "% voted for Yes")
                Server.Broadcast(str(min) + "% was needed for a Ban")
            DataStore.Add("Vote", "PB.SysTick", System.Environment.TickCount)
        elif ttype == "PK":
            min = DataStore.Get("Vote", "PK.Min")
            if pyes >= min:
                Server.Broadcast("The results are in and " + self.targetname + " has been kicked from the server!")
                Server.Broadcast(str(pyes) + "% voted for Yes")
                Server.Broadcast(str(pno) + "% voted for No")
                self.disconnectplayer("Players have voted to kick you!")
            else:
                Server.Broadcast("The results are in and " + self.targetname + " has not been kicked from the server!")
                Server.Broadcast(str(pyes) + "% voted for Yes")
                Server.Broadcast(str(min) + "% was needed for a Kick")
            DataStore.Add("Vote", "PK.SysTick", System.Environment.TickCount)
        elif ttype[0] == "CUSTOM":
                Server.Broadcast("The results are in for: " + ttype[1])
                Server.Broadcast(str(pyes) + "% voted for Yes")
                Server.Broadcast(str(pno) + "% voted for No")
        else:
            min = DataStore.Get("Vote", "AD.Min")
            if pyes > min:
                World.AirDrop()
                Server.Broadcast("The results are in and an AirDrop is on its way!")
                Server.Broadcast(str(pyes) + "% voted for Yes")
            else:
                Server.Broadcast("The results are in and an AirDrop has not been called in!")
                Server.Broadcast(str(pno) + "% voted for No")
            DataStore.Add("Vote", "AD.SysTick", System.Environment.TickCount)
        DataStore.Remove("Vote", "type")
        self.removevotes()

    def playerscheck(self, Player, ttype):
        if Player.Owner:
            return True
        elif Player.Admin:
            return True
        elif Player.Moderator:
            return True
        elif DataStore.Get("Vote", ttype + ".PCU") == "true":
            return True
        else:
            return False

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "vote":
            if len(args) == 0:
                Player.Message("/vote [yes/no] - Votes for yes or no")
                if self.playerscheck(Player, "D/N"):
                    Player.Message("/vote day - Vote for day")
                if self.playerscheck(Player, "AD"):
                    Player.Message("/vote airdrop - Vote for an airdrop")
                if self.playerscheck(Player, "PB"):
                    Player.Message("/vote ban [Name] - Vote to ban a player")
                if self.playerscheck(Player, "PK"):
                    Player.Message("/vote kick [Name] - Vote to kick a player")
                if self.playerscheck(Player, "CUSTOM"):
                    Player.Message('/vote custom [Insert a question here] - Ask a custom question')
                if self.playerscheck(Player, "STOP"):
                    Player.Message('/vote stop - Stops the current vote')
            else:
                if args[0] == "yes":
                    if Plugin.GetTimer("VoteTimer") is not None:
                        if DataStore.Get("VoteNO", Player.SteamID) is not None:
                            DataStore.Remove("VoteNO", Player.SteamID)
                            DataStore.Add("VoteYES", Player.SteamID, "yes")
                            Player.Message("You have changed your vote to Yes")
                        elif DataStore.Get("VoteYES", Player.SteamID) is not None:
                            Player.Message("You have already voted for Yes")
                        else:
                            DataStore.Add("VoteYES", Player.SteamID, "yes")
                            Player.Message("You have voted for Yes")
                    else:
                        Player.Message("There is no vote in progress!")
                elif args[0] == "no":
                    if Plugin.GetTimer("VoteTimer") is not None:
                        if DataStore.Get("VoteYES", Player.SteamID) is not None:
                            DataStore.Remove("VoteYES", Player.SteamID)
                            DataStore.Add("VoteNO", Player.SteamID, "no")
                            Player.Message("You have changed your vote to No")
                        elif DataStore.Get("VoteNO", Player.SteamID) is not None:
                            Player.Message("You have already voted for No")
                        else:
                            DataStore.Add("VoteNO", Player.SteamID, "no")
                            Player.Message("You have voted for No")
                    else:
                        Player.Message("There is no vote in progress!")
                elif args[0] == "stop":
                    if self.playerscheck(Player, "STOP"):
                        if Plugin.GetTimer("VoteTimer") is not None:
                            DataStore.Remove("Vote", "type")
                            self.removevotes()
                            Server.Broadcast("An Admin has stopped the current vote!")
                        else:
                            Player.Message("There currently is no vote running!")
                    else:
                        Player.Message("You are not allowed to use this command!")
                elif args[0] == "airdrop":
                    if self.playerscheck(Player, "AD"):
                        if len(Server.Players) >= DataStore.Get("Vote", "AD.MPlayers"):
                            if Plugin.GetTimer("VoteTimer") is None:
                                waittime = DataStore.Get("Vote", "AD.Cooldown")
                                time = DataStore.Get("Vote", "AD.SysTick")
                                if time is None:
                                    time = 0
                                else:
                                    time = int(time)
                                calc = System.Environment.TickCount - time
                                if calc >= waittime or Player.Owner or Player.Admin:
                                    try:
                                        Plugin.CreateTimer("VoteTimer", DataStore.Get("Vote", "AD.VoteLength")).Start()
                                        DataStore.Add("Vote", "type", "AD")
                                        Server.Broadcast("Would you like an airdrop?")
                                        Server.Broadcast("You have " + str(DataStore.Get("Vote", "AD.VoteLength") / 1000) + " seconds to vote")
                                        Server.Broadcast("How to vote: /vote [Yes/No]")
                                    except:
                                        Player.Message("Error, Try again")
                                else:
                                    workingout = (round(waittime / 1000, 2) / 60) - round(int(calc) / 1000, 2) / 60
                                    current = round(workingout, 2)
                                    Player.Message(str(current) + " Minutes remaining before you can use this.")
                            else:
                                Player.Message("There is already vote in progress!")
                        else:
                            Player.Message("Not enough players online")
                    else:
                        Player.Message("You are not allowed to use this command!")
                elif args[0] == "day":
                    canuse = False
                    if self.playerscheck(Player, "D/N"):
                        if DataStore.Get("Vote", "D/N.CanUse") == "true":
                            canuse = True
                        if 17 < World.Time or World.Time < 5 or canuse:
                            if len(Server.Players) >= DataStore.Get("Vote", "D/N.MPlayers"):
                                if Plugin.GetTimer("VoteTimer") is None:
                                    waittime = DataStore.Get("Vote", "D/N.Cooldown")
                                    time = DataStore.Get("Vote", "D/N.SysTick")
                                    if time is None:
                                        time = 0
                                    else:
                                        time = int(time)
                                    calc = System.Environment.TickCount - time
                                    if calc >= waittime or Player.Owner or Player.Admin:
                                        try:
                                            DataStore.Add("Vote", "type", "D/N")
                                            Plugin.CreateTimer("VoteTimer", DataStore.Get("Vote", "D/N.VoteLength")).Start()
                                            Server.Broadcast("Would you like the time to be morning?")
                                            Server.Broadcast("You have " + str(DataStore.Get("Vote", "D/N.VoteLength") / 1000) + " seconds to vote")
                                            Server.Broadcast("How to vote: /vote [Yes/No]")
                                        except:
                                            Player.Message("Error, Try again")
                                    else:
                                        workingout = (round(waittime / 1000, 2) / 60) - round(int(calc) / 1000, 2) / 60
                                        current = round(workingout, 2)
                                        Player.Message(str(current) + " Minutes remaining before you can use this.")
                                else:
                                    Player.Message("There is already vote in progress!")
                            else:
                                Player.Message("Not enough players online")
                        else:
                            Player.Message("Wait until its night!")
                    else:
                        Player.Message("You are not allowed to use this command!")
                elif args[0] == "ban":
                    if self.playerscheck(Player, "PB"):
                        if len(Server.Players) >= DataStore.Get("Vote", "PB.MPlayers"):
                            if Plugin.GetTimer("VoteTimer") is None:
                                try:
                                    ban = self.CheckV(Player, args[1])
                                except:
                                    Player.Message("Usage: /vote ban [Players Name]")
                                    return
                                if ban is not None:
                                    if ban.Name is not Player.Name:
                                        if not ban.Owner or ban.Admin or ban.Moderator:
                                            waittime = DataStore.Get("VoteBan", "PB.Cooldown")
                                            time = DataStore.Get("VoteBan", "PB.SysTick")
                                            if time is None:
                                                time = 0
                                            else:
                                                time = int(time)
                                            calc = System.Environment.TickCount - time
                                            if calc >= waittime or Player.Owner or Player.Admin or Player.Moderator:
                                                try:
                                                    self.target = ban
                                                    self.targetname = ban.Name
                                                    self.targetip = ban.IP
                                                    self.targetid = ban.GameID
                                                    DataStore.Add("Vote", "type", "PB")
                                                    Plugin.CreateTimer("VoteTimer", DataStore.Get("Vote", "PB.VoteLength")).Start()
                                                    Server.Broadcast("Should we ban: " + ban.Name + "?")
                                                    Server.Broadcast("You have " + str(DataStore.Get("Vote", "PB.VoteLength") / 1000) + " seconds to vote")
                                                    Server.Broadcast("How to vote: /vote [Yes/No]")
                                                    ban.Message("If you disconnect you WILL be banned!")
                                                except:
                                                    Player.Message("Error, Try again")
                                            else:
                                                workingout = (round(waittime / 1000, 2) / 60) - round(int(calc) / 1000, 2) / 60
                                                current = round(workingout, 2)
                                                Player.Message(str(current) + " Minutes remaining before you can use this.")
                                        else:
                                            Player.Message("That player is a staff member!")
                                    else:
                                        Player.Message("You can not ban yourself!")
                                else:
                                    return
                            else:
                                Player.Message("There is already vote in progress!")
                        else:
                            Player.Message("Not enough players online")
                    else:
                        Player.Message("You are not allowed to use this command!")
                elif args[0] == "kick":
                    if self.playerscheck(Player, "PK"):
                        if len(Server.Players) >= DataStore.Get("Vote", "PK.MPlayers"):
                            if Plugin.GetTimer("VoteTimer") is None:
                                try:
                                    kick = self.CheckV(Player, args[1])
                                except:
                                    Player.Message("Usage: /vote kick [Players Name]")
                                    return
                                if kick is not None:
                                    if kick.Name is not Player.Name:
                                        if not kick.Owner or kick.Admin or kick.Moderator:
                                            waittime = DataStore.Get("VoteBan", "PK.Cooldown")
                                            time = DataStore.Get("VoteBan", "PK.SysTick")
                                            if time is None:
                                                time = 0
                                            else:
                                                time = int(time)
                                            calc = System.Environment.TickCount - time
                                            if calc >= waittime or Player.Owner or Player.Admin or Player.Moderator:
                                                try:
                                                    self.target = kick
                                                    self.targetname = kick.Name
                                                    self.targetip = kick.IP
                                                    self.targetid = kick.GameID
                                                    DataStore.Add("Vote", "type", "PK")
                                                    Plugin.CreateTimer("VoteTimer", DataStore.Get("Vote", "PK.VoteLength")).Start()
                                                    Server.Broadcast("Should we kick: " + kick.Name + "?")
                                                    Server.Broadcast("You have " + str(DataStore.Get("Vote", "PK.VoteLength") / 1000) + " seconds to vote")
                                                    Server.Broadcast("How to vote: /vote [Yes/No]")
                                                except:
                                                    Player.Message("Error, Try again")
                                            else:
                                                workingout = (round(waittime / 1000, 2) / 60) - round(int(calc) / 1000, 2) / 60
                                                current = round(workingout, 2)
                                                Player.Message(str(current) + " Minutes remaining before you can use this.")
                                        else:
                                            Player.Message("That player is a staff member!")
                                    else:
                                        Player.Message("You can not kick yourself!")
                                else:
                                    return
                            else:
                                Player.Message("There is already vote in progress!")
                        else:
                            Player.Message("Not enough players online")
                    else:
                        Player.Message("You are not allowed to use this command!")
                elif args[0] == "custom":
                    if self.playerscheck(Player, "Custom"):
                        if Plugin.GetTimer("VoteTimer") is None:
                            if len(args) > 1:
                                question = self.joinquestion(args)
                                DataStore.Add("Vote", "type", "CUSTOM:" + question)
                                Plugin.CreateTimer("VoteTimer", 60000).Start()
                                Server.Broadcast("An admin asked:" + question)
                                Server.Broadcast("You have 60 seconds to vote")
                                Server.Broadcast("How to vote: /vote [Yes/No]")
                            else:
                                Player.Message('Usage: /vote custom [Insert a question here]')
                        else:
                            Player.Message("There is already vote in progress!")
                    else:
                        Player.Message("You are not allowed to use this command!")
                else:
                    Player.Message("/vote [yes/no] - Votes for yes or no")
                    if self.playerscheck(Player, "D/N"):
                        Player.Message("/vote day - Vote for day")
                    if self.playerscheck(Player, "AD"):
                        Player.Message("/vote airdrop - Vote for an airdrop")
                    if self.playerscheck(Player, "PB"):
                        Player.Message("/vote ban [Name] - Vote to ban a player")
                    if self.playerscheck(Player, "PK"):
                        Player.Message("/vote kick [Name] - Vote to kick a player")
                    if self.playerscheck(Player, "CUSTOM"):
                        Player.Message('/vote custom [Insert a question here] - Ask a custom question')
                    if self.playerscheck(Player, "STOP"):
                        Player.Message('/vote stop - Stops the current vote')
        return

    def joinquestion(self, args):
        args[0] = None
        s = str.Join(" ", args)
        return s

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name):
        Name = name.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == Name:
                return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V5.0
        --REMOVED OFFLINE PLAYER CHECK (Unused code for this plugin)--
    """

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args))
            if p is not None:
                return p
            else:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            else:
                for pl in Server.ActivePlayers:
                    if str(args).lower() in pl.Name.lower():
                        p = pl
                        count += 1
        if count == 0:
            Player.MessageFrom("Vote", "Couldn't find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("Vote", "Found " + str(count) + " player with similar name. Use more correct name!")
            return None



