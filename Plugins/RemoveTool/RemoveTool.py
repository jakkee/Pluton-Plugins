__title__ = 'RemoveTool'
__author__ = 'Jakkee'
__version__ = '1.1.1'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp", "UnityEngine")
import Pluton
import BuildingPrivlidge
import ItemManager
import UnityEngine

 
class RemoveTool:
    def Tryint(self, Arg):
        try:
            time = int(Arg)
            return time
        except:
            return 180

    def On_PluginInit(self):
        Commands.Register("remove")\
            .setCallback("remove")\
            .setDescription("Removes an entity")\
            .setUsage("/remove [Time]")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "MaxRemoveSeconds", "180")
            ini.AddSetting("Messages", "ActivatedMSG", "Activated for %TIME% seconds")
            ini.AddSetting("Messages", "DeactivatedMSG", "Deactivated")
            ini.AddSetting("Messages", "NoToolCupboard", "Place a Tool Cupboard first!")
            ini.AddSetting("Messages", "NoBuildPrivlidge", "You do not have full BuildingPrivlidge here!")
            ini.AddSetting("Messages", "OutOfRange", "You're too far away to destroy this!")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("RemoveTool")
        DataStore.Add("RemoveTool", "MRS", self.Tryint(ini.GetSetting("Settings", "MaxRemoveSeconds")))
        DataStore.Add("RemoveTool", "AMSG",ini.GetSetting("Messages", "ActivatedMSG"))
        DataStore.Add("RemoveTool", "DMSG",ini.GetSetting("Messages", "DeactivatedMSG"))
        DataStore.Add("RemoveTool", "NTC",ini.GetSetting("Messages", "NoToolCupboard"))
        DataStore.Add("RemoveTool", "NBP",ini.GetSetting("Messages", "NoBuildPrivlidge"))
        DataStore.Add("RemoveTool", "OFR",ini.GetSetting("Messages", "OutOfRange"))

    def RemoveToolCallback(self, timer):
        data = timer.Args
        playerID = data["PlayerID"]
        Player = Server.Players[playerID]
        if DataStore.Get("Remove", Player.SteamID) is None:
            timer.Kill()
            return
        elif Player is not None:
            DataStore.Remove("Remove", Player.SteamID)
            Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "DMSG"))
        timer.Kill()

    def intcheck(self, i):
        try:
            maxx = DataStore.Get("RemoveTool", "MRS")
            i = int(i)
            if i >= maxx:
                i = maxx
            elif i <= 30:
                i = 30
            return i
        except:
            return 30
        
    def remove(self, args, Player):
        if len(args) == 1:
            if DataStore.Get("Remove", Player.SteamID) is not None:
                DataStore.Remove("Remove", Player.SteamID)
                Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "DMSG"))
                for timer in Plugin.GetParallelTimer("RemoveTool"):
                    if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                        timer.Kill()
            else:
                DataStore.Add("Remove", Player.SteamID, "Remove")
                time = self.intcheck(args[0]) * 1000
                RemoveTool = Plugin.CreateDict()
                RemoveTool["PlayerID"] = Player.GameID
                Plugin.CreateParallelTimer("RemoveTool", time, RemoveTool).Start()
                time = str(time / 1000)
                Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "AMSG").replace('%TIME%', time))
        else:
            if DataStore.Get("Remove", Player.SteamID) is not None:
                DataStore.Remove("Remove", Player.SteamID)
                Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "DMSG"))
                for timer in Plugin.GetParallelTimer("RemoveTool"):
                    if Server.Players[timer.Args["PlayerID"]].SteamID == Player.SteamID:
                        timer.Kill()
            else:
                DataStore.Add("Remove", Player.SteamID, "Remove")
                time = 30000
                RemoveTool = Plugin.CreateDict()
                RemoveTool["PlayerID"] = Player.GameID
                Plugin.CreateParallelTimer("RemoveTool", time, RemoveTool).Start()
                time = "30"
                Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "AMSG").replace('%TIME%', time))

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
                    if Util.GetVectorsDistance(Player.Location, privlidge.transform.position) <= float(30.1):
                        tcCount += 1
                        if privlidge.IsAuthed(Player.basePlayer):
                            poCount += 1
                if tcCount == 0:
                    Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "NTC"))
                elif poCount < tcCount:
                    Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "NBP"))
                else:
                    if Util.GetVectorsDistance(CombatEntityHurtEvent.Victim.Location, Player.Location) <= float(3.5):
                        try:
                            for x in CombatEntityHurtEvent.Victim.ToBuildingPart().buildingBlock.currentGrade.costToBuild:
                                Player.Inventory.Add(x.itemid, x.amount)
                                CombatEntityHurtEvent.Victim.Kill()
                                return
                        except:
                            try:
                                item = ItemManager.FindItemDefinition(CombatEntityHurtEvent.Victim.baseEntity.LookupShortPrefabName())
                                Player.Inventory.Add(item.itemid, 1)
                                Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                            except:
                                Data = {}
                                Data['woodbox_deployed'] = 'box_wooden'
                                Data['large_woodbox_deployed'] = 'box_wooden_large'
                                Data['campfire_deployed'] = 'campfire'
                                Data['crudeoutput'] = 'mining.pumpjack'
                                Data['hopperoutput'] = 'mining.guarry'
                                Data['cupboard.tool.deployed'] = 'cupboard.tool'
                                Data['furnace_deployed'] = 'furnace'
                                Data['lantern_deployed'] = 'lantern'
                                Data['large_furnace_deployed'] = 'large_furnace'
                                Data['repairbench_deployed'] = 'box_repair_bench'
                                Data['researchtable_deployed'] = 'research_table'
                                Data['sign.huge.wood'] = 'sign.wooden.huge'
                                Data['sign.large.wood'] = 'sign.wooden.large'
                                Data['sign.medium.wood'] = 'sign.wooden.medium'
                                Data['sign.small.wood'] = 'sign.wooden.small'
                                Data['sleepingbag_leather_deployed'] = 'sleepingbag'
                                Data['refinery_small_deployed'] = 'small_oil_refinery'
                                Data['beartrap'] = 'trap_bear'
                                Data['landmine'] = 'trap_landmine'
                                Data['floor_spikes'] = 'spikes.floor'
                                Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                item = ItemManager.FindItemDefinition(Data[CombatEntityHurtEvent.Victim.baseEntity.LookupShortPrefabName()])
                                Player.Inventory.Add(item.itemid, 1)
                        return
                    else:
                        Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "OFR"))
        return
        
