__title__ = 'SleeperTP'
__author__ = 'Jakkee'
__about__ = 'Teleport to sleepers'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton

 
class SleeperTP:

    TPHistory = {}

    def On_PluginInit(self):
        Commands.Register("sleeper")\
            .setCallback("sleeper")\
            .setDescription("Teleport to a sleeper")\
            .setUsage("/sleeper next")

    def sleeper(self, args, Player):
        if Player.Admin:
            if len(args) == 0:
                Player.Message("/sleeper next")
                Player.Message("/sleeper reset")
                Player.Message("/sleeper [Name]")
            elif args[0] == "next":
                if not len(Server.OfflinePlayers.Values) == 0:
                    if not len(self.TPHistory) == len(Server.OfflinePlayers.Values):
                        for sleeper in Server.OfflinePlayers.Values:
                            try:
                                if self.TPHistory[sleeper.SteamID] == sleeper.SteamID:
                                    continue
                            except:
                                Player.Teleport(sleeper.X, sleeper.Y, sleeper.Z)
                                self.TPHistory[sleeper.SteamID] = sleeper.SteamID
                                Player.Message("You have teleported to: " + sleeper.Name + " = " + sleeper.SteamID)
                                break
                            else:
                                continue
                    else:
                        Player.Message("You have teleported to all the sleepers on the server")
                        Player.Message("Type: /sleeper reset  to clear the sleeper tp history")
                else:
                    Player.Message("You have zero sleepers on your server!")
            elif args[0] == "reset":
                self.TPHistory = {}
                Player.Message("Teleport history reset!")
            else:
                target = self.CheckV(Player, args)
                if target is not None:
                    Player.Teleport(target.X, target.Y, target.Z)
                    Player.Message("You have teleported to: " + target.Name + " = " + target.SteamID)
                else:
                    return
        else:
            Player.Message("You are not allowed to use this command!")             
                    
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

    def GetPlayerName(self, name):
        Name = name.lower()
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
            else:
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
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.Message("Couldn't find sleeper" + str.Join(" ", args) + "! Maybe he/she is awake?")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " sleepers with a similar name. Use a more correct name!")
            return None