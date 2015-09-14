__title__ = 'Prefix'
__author__ = 'Jakkee'
__about__ = 'Add prefixs to players'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton
 
 
class Prefix:
    def On_PluginInit(self):
        Commands.Register("prefix")\
            .setCallback("prefix")\
            .setDescription("Adds prefix to players")\
            .setUsage("/prefix [add/remove] [PlayerName] [Prefix] [Chat Color]")
        if not Plugin.IniExists("Users"):
            Plugin.CreateIni("Users")
            ini = Plugin.GetIni("Users")
            ini.Save()
        DataStore.Flush("Prefix")
        ini = Plugin.GetIni("Users")
        for id in ini.EnumSection("Users"):
            key = ini.GetSetting("Users", id).split(':')
            DataStore.Add("Prefix", id + ":Prefix", key[0])
            DataStore.Add("Prefix", id + ":Colour", key[1])        

    def prefix(self, args, Player):
        if Player.Owner or Player.Admin:
            if len(args) == 0:
                Player.Message('Usage: /prefix [add] [PlayerName] [Prefix] [ChatColor]')
                Player.Message('Usage: /prefix [remove] [PlayerName]')
            elif args[0] == "add":
                if len(args) == 4:
                    target = self.CheckV(Player, args[1])
                    if target is not None:
                        check = self.FindPrefix(target)
                        if not check[0]:
                            prefix = args[2]
                            colour = args[3]
                            ini = Plugin.GetIni("Users")
                            ini.AddSetting("Users", target.SteamID, prefix + ":" + colour)
                            ini.Save()
                            DataStore.Add("Prefix", target.SteamID + ":Prefix", prefix)
                            DataStore.Add("Prefix", target.SteamID + ":Colour", colour)
                            target.Message("You now have a prefix: " + prefix)
                            Player.Message("Added " + prefix + " to " + target.Name)
                        else:
                            Player.Message(target.Name + " already has a prefix: " + check[1] + " Delete it before changing")
                    else:
                        return
                else:
                    Player.Message('Example: /prefix add "Newbie Player" [VIP] #FFFFFF')
            elif args[0] == "remove":
                if len(args) == 2:
                    target = self.CheckV(Player, args[1])
                    if target is not None:
                        check = self.FindPrefix(target)
                        if check[0]:
                            ini = Plugin.GetIni("Users")
                            ini.DeleteSetting("Users", target.SteamID)
                            ini.Save()
                            DataStore.Remove("Prefix", target.SteamID + ":Prefix")
                            DataStore.Remove("Prefix", target.SteamID + ":Colour")
                            Player.Message(target.Name + "'s prefix has been removed!")
                            target.Message("Your prefix has been removed!")
                        else:
                            Player.Message(target.Name + " does not have a prefix!")
                    else:
                        return
                else:
                    Player.Message('Example: /prefix remove "Newbie Player"')
            else:
                Player.Message('Usage: /prefix [add] [PlayerName] [Prefix] [ChatColor]')
                Player.Message('Usage: /prefix [remove] [PlayerName]')
        else:
            Player.Message("You are not allowed to use that command!")

    def On_PlayerConnected(self, Player):
        if DataStore.Get("Prefix", "JoinMMSG") == "true":
            try:
                found = self.FindPrefix(Player)
            except:
                found = False, None
            if found[0]:
                Server.BroadcastFrom(found[1], Player.Name + " is now Online.")
            else:
                Server.Broadcast(Player.Name + " is now Online!")
 
    def On_PlayerDisconnected(self, Player):
        if DataStore.Get("Prefix", "LeaveMMSG") == "true":
            try:
                found = self.FindPrefix(Player)
            except:
                found = False, None, None
            if found[0]:
                Server.BroadcastFrom(found[1], Player.Name + " is now Offline.")
            else:
                Server.Broadcast(Player.Name + " is now Offline!")

    def FindPrefix(self, Player):
        prefix = DataStore.Get("Prefix", Player.SteamID + ":Prefix")
        colour = DataStore.Get("Prefix", Player.SteamID + ":Colour")
        if prefix and colour is not None or "":
            return True, prefix, colour
        else:
            return False, None, None
 
    def On_Chat(self, ChatEvent):
        Player = ChatEvent.User
        try:
            found = self.FindPrefix(Player)
        except:
            found = False, None, None
        if found[0]:
            Server.BroadcastFrom(found[1] + Player.Name, "<color=" + found[2] + ">" + ChatEvent.OriginalText + "</color>")
            ChatEvent.FinalText = ""

    def GetPlayerName(self, name):
        Name = name.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == Name:
                return pl
        for pl in Server.OfflinePlayers.Values:
            if pl.Name.lower() == Name:
                return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        Mode: Search mode (Default: 1)
            1 = Search Online Players
            2 = Search Offline Players
            3 = Both
        V5.0
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
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
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
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.Message("Couldn't find player: " + args)
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " player with similar name. Use more correct name!")
            return None
