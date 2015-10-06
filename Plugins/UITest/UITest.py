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
    raise ImportError("UI TEST: Can not find JSON in Libs folder [Pluton\Python\Libs\] *DOWNLOAD: http://forum.pluton-team.org/resources/microjson.54/*")
broadcastgui = [
    {
        "name": "broadcastui",
        #"parent": "Overlay",
        "components":
        [
            {
                "type": "UnityEngine.UI.Image",
                "color": "0.1 0.1 0.1 0.3",
            },
            {
                "type": "RectTransform",
                "anchormin": "0.3 0.95",
                "anchormax": "0.7 0.995"
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


class UITEST:
    def On_Command(self, CommandEvent):
        Player = CommandEvent.User
        cmd = CommandEvent.Cmd
        args = CommandEvent.Args
        if cmd == "show":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /show <insert your message here>")
                else:
                    timer = Plugin.GetTimer("RemoveBroadcast")
                    if timer is not None:
                        timer.Kill()
                    self.SetBroadcast(str.Join(" ", args))
                    Plugin.CreateTimer("RemoveBroadcast", 8000).Start()
            else:
                Player.MessageFrom("Error", "You do not have permission to use this command!")
        elif cmd == "hide":
            if Player.Admin:
                for p in Server.ActivePlayers:
                    CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(p.basePlayer.net.connection), None, "DestroyUI", Facepunch.ObjectList("broadcastui"))
                Player.Message("UI's Removed")
            else:
                Player.MessageFrom("Error", "You do not have permission to use this command!")

    def SetBroadcast(self, args):
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None, "AddUI", Facepunch.ObjectList(broadcast.Replace("[TEXT]", args)))

    def RemoveBroadcastCallback(self, timer):
        timer.Kill()
        for Player in Server.ActivePlayers:
            CommunityEntity.ServerInstance.ClientRPCEx(Network.SendInfo(Player.basePlayer.net.connection), None,
                                                   "DestroyUI", Facepunch.ObjectList("broadcastui"))
