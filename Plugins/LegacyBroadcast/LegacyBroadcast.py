__title__ = 'LegacyBroadcast'
__author__ = 'Jakkee'
__about__ = 'Broadcast test to your server, Legacy style!'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp-firstpass", "Assembly-CSharp")
import Facepunch
import CommunityEntity
import Network
import Pluton
import sys
path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")
try:
    import json
except ImportError:
    raise ImportError("LegacyBroadcast: Can not find JSON in Libs folder [Pluton\Python\Libs\] *DOWNLOAD: http://forum.pluton-team.org/resources/microjson.54/*")
broadcastgui = [
    {
        "name": "broadcastui",
        #"parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.4",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.005 0.965",
                "anchormax": "0.995 0.995"
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
                "anchormin": "0.005 0.005",
                "anchormax": "0.995 0.995"
            }
        ]
    }
]
string = json.encode(broadcastgui)
broadcast = json.makepretty(string)


class LegacyBroadcast:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "Command", "/say")
            ini.AddSetting("Settings", "Popup time", "10")
            ini.AddSetting("Allowed Ranks", "Users", "false")
            ini.AddSetting("Allowed Ranks", "Moderators", "true")
            ini.AddSetting("Allowed Ranks", "Admins", "true")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("BroadCast", "Timer", int(ini.GetSetting("Settings", "Popup time")) * 1000)
        DataStore.Add("BroadCast", "Users", ini.GetBoolSetting("Allowed Ranks", "Users"))
        DataStore.Add("BroadCast", "Mod", ini.GetBoolSetting("Allowed Ranks", "Moderators"))
        DataStore.Add("BroadCast", "Admin", ini.GetBoolSetting("Allowed Ranks", "Admins"))
        DataStore.Add("BroadCast", "Command", ini.GetSetting("Settings", "Command").Replace("/", ""))
        command = ini.GetSetting("Settings", "Command").Replace("/", "")
        Commands.Register(command).setCallback("command")
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("broadcastui"))

    def isAllowed(self, Player):
        if Player.Admin or Player.Owner:
            if DataStore.Get("BroadCast", "Admin"):
                return True
            else:
                return False
        elif Player.Moderator:
            if DataStore.Get("BroadCast", "Mod"):
                return True
            else:
                return False
        elif DataStore.Get("BroadCast", "Users"):
            return True
        else:
            return False            

    def command(self, args, Player):
        if self.isAllowed(Player):
            if len(args) == 0:
                Player.Message("Usage: /" + DataStore.Get("BroadCast", "Command") +" <insert your message here>")
            else:
                timer = Plugin.GetTimer("RemoveBroadcast")
                if timer is not None:
                    timer.Kill()
                self.SetBroadcast(str.Join(" ", args))
                Plugin.CreateTimer("RemoveBroadcast", int(DataStore.Get("BroadCast", "Timer"))).Start()
        else:
            Player.Message("You do not have permission to use this command!")

    def SetBroadcast(self, args):
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("broadcastui"))
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", Facepunch.ObjectList(broadcast.Replace("[TEXT]", args)))

    def RemoveBroadcastCallback(self, timer):
        timer.Kill()
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("broadcastui"))
