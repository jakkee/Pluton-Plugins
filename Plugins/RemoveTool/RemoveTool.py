__title__ = 'RemoveTool'
__author__ = 'Jakkee'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
clr.AddReferenceByPartialName("UnityEngine")
import Pluton
import BuildingPrivlidge
import WorldItem
import UnityEngine

 
class RemoveTool:
    def RemoveToolCallback(self, timer):
        data = timer.Args
        playerID = data["PlayerID"]
        Player = Server.Players[playerID]
        if DataStore.Get("Remove", Player.SteamID) is None:
            timer.Kill()
            return
        elif Player is not None:
            DataStore.Remove("Remove", Player.SteamID)
            Player.MessageFrom("RemoveTool", "Deactivated")
        timer.Kill()

    def intcheck(self, i):
        try:
            i = int(i)
            if i >= 180:
                i = 180
            elif i <= 30:
                i = 30
            return i
        except:
            return 30
        
    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        c = cmd.cmd
        if c == "remove":
            if len(args) == 1:
                if DataStore.Get("Remove", Player.SteamID) is not None:
                    DataStore.Remove("Remove", Player.SteamID)
                    Player.MessageFrom("RemoveTool", "Deactivated")
                    for timer in Plugin.GetParallelTimer("RemoveTool"):
                        if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                            timer.Kill()
                else:
                    DataStore.Add("Remove", Player.SteamID, "Remove")
                    time = self.intcheck(args[0]) * 1000
                    RemoveTool = Plugin.CreateDict()
                    RemoveTool["PlayerID"] = Player.GameID
                    Plugin.CreateParallelTimer("RemoveTool", time, RemoveTool).Start()
                    Player.MessageFrom("RemoveTool", "Activated for " + str(time / 1000) + " seconds")
            else:
                if DataStore.Get("Remove", Player.SteamID) is not None:
                    DataStore.Remove("Remove", Player.SteamID)
                    Player.MessageFrom("RemoveTool", "Deactivated")
                    for timer in Plugin.GetParallelTimer("RemoveTool"):
                        if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                            timer.Kill()
                else:
                    DataStore.Add("Remove", Player.SteamID, "Remove")
                    time = 30000
                    RemoveTool = Plugin.CreateDict()
                    RemoveTool["PlayerID"] = Player.GameID
                    Plugin.CreateParallelTimer("RemoveTool", time, RemoveTool).Start()
                    Player.MessageFrom("RemoveTool", "Activated for " + str(time / 1000) + " seconds")

    def On_CombatEntityHurt(self, CombatEntityHurtEvent):
        try:
            Player = CombatEntityHurtEvent.Attacker.ToPlayer()
            BuildingPart = CombatEntityHurtEvent.Victim.ToBuildingPart()
        except:
            return
        if Player is not None:
            if DataStore.Get("Remove", Player.SteamID) is not None:
                tcCount = 0
                poCount = 0
                for privlidge in UnityEngine.Object.FindObjectsOfType[BuildingPrivlidge]():
                    if Util.GetVectorsDistance(Player.Location, privlidge.transform.position) <= float(50):
                        tcCount += 1
                        if privlidge.IsAuthed(Player.basePlayer):
                            poCount += 1
                if tcCount == 0:
                    Player.Message("Place a Tool Cupboard first!")
                elif poCount < tcCount:
                    Player.Message("You do not have full BuildingPrivlidge here!")
                else:
                    if Util.GetVectorsDistance(CombatEntityHurtEvent.Victim.Location, Player.Location) <= float(3.5):
                        try:
                            for x in CombatEntityHurtEvent.Victim.ToBuildingPart().buildingBlock.currentGrade.costToBuild:
                                Player.Inventory.Add(x.itemid, x.amount)
                                CombatEntityHurtEvent.Victim.Kill()
                            return
                        except:
                            try:
                                item = Find.ItemDefinition(CombatEntityHurtEvent.Victim.baseEntity.panelName)
                                Player.Inventory.Add(item.itemid, 1)
                                CombatEntityHurtEvent.Victim.Kill()
                                return
                            except:
                                name = CombatEntityHurtEvent.Victim.Name
                                if name == "cupboard.tool.deployed(Clone)" or name == "items/cupboard.tool.deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Tool Cupboard", 1)
                                elif name == "signs/sign.small.wood":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Small Wooden Sign", 1)
                                elif name == "signs/sign.medium.wood":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Wooden Sign", 1)
                                elif name == "signs/sign.large.wood":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Large Wooden Sign", 1)
                                elif name == "signs/sign.huge.wood":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Huge Wooden Sign", 1)
                                elif name == "large_woodbox_deployed(Clone)" or name == "items/large_woodbox_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Large Wood Box", 1)
                                elif name == "woodbox_deployed(Clone)" or name == "items/woodbox_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Wood Storage Box", 1)
                                elif name == "items/furnace_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Furnace", 1)
                                elif name == "items/campfire_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Campfire", 1)
                                elif name == "repairbench_deployed(Clone)" or name == "items/repairbench_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Repair Bench", 1)
                                elif name == "items/sleepingbag_leather_deployed":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Sleeping Bag", 1)
                                elif name == "beartrap(Clone)" or name == "items/beartrap(Clone)":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("trap_bear", 1)
                                elif name == "items/barricades/barricade.woodwire":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Barbed Wooden Barricade", 1)
                                elif name == "items/barricades/barricade.metal":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Metal Barricade", 1)
                                elif name == "items/barricades/barricade.wood":
                                    Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    Player.Inventory.Add("Wooden Barricade", 1)
                                else:
                                    #Player.Message(name)
                                    return
                        return
                    else:
                        Player.Message("You're too far away to destroy this!")
        return
