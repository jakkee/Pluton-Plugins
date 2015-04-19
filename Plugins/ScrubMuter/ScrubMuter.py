__title__ = 'ScrubMuter'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class ScrubMuter:
    def On_Chat(self, ChatEvent):
        Player = ChatEvent.User
        if Plugin.GetIni("Scrubs").GetSetting("MutedScrubs", Player.SteamID) == "muted":
            Util.Log(Player.Name + " is muted and chat message was not sent")
            ChatEvent.FinalText = ""
            Player.Message("You are muted!")

    def On_Command(self, command):
        Player = command.User
        if command.cmd == "mute":
            if Player.Owner or Player.Admin or Player.Moderator:
                if len(command.args) == 0:
                    Player.Message("/mute [Player] - Mutes a player")
                    Player.Message("/unmute [Player] - unmutes a player")
                else:
                    playerr = self.CheckV(Player, command.args[0])
                    if playerr is None:
                        return
                    if not Plugin.IniExists("Scrubs"):
                        Plugin.CreateIni("Scrubs")
                        Plugin.GetIni("Scrubs").Save()
                    ini = Plugin.GetIni("Scrubs")
                    ini.AddSetting("MutedScrubs", playerr.SteamID, "muted")
                    ini.Save()
                    Server.Broadcast(playerr.Name + " has been muted by: " + Player.Name)
            else:
                Player.Message("You are not allowed to use that command!")
        elif command.cmd == "unmute":
            if Player.Owner or Player.Admin or Player.Moderator:
                if len(command.args) == 0:
                    Player.Message("/mute [Player] - Mutes a player")
                    Player.Message("/unmute [Player] - unmutes a player")
                else:
                    playerr = self.CheckV(Player, command.args[0])
                    if playerr is None:
                        return
                    ini = Plugin.GetIni("Scrubs")
                    ini.DeleteSetting("MutedScrubs", playerr.SteamID)
                    ini.Save()
                    Server.Broadcast(playerr.Name + " has been unmuted by: " + Player.Name)
            else:
                Player.Message("You are not allowed to use that command!")

#DreTaX's methods here
    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            s = str(args).lower()
            for pl in Server.ActivePlayers:
                if s in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.Message("Couldn't find " + String.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " player with similar name. Use more correct name!")
            return None
