__title__ = 'RemoveTool'
__author__ = 'Jakkee'
__about__ = 'Remove entitys'
__version__ = '1.1.2'

import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp", "UnityEngine")
import Pluton
import BuildingPrivlidge
import ItemManager
import UnityEngine


 
class RemoveTool:
    Data = {}
    Data['woodbox_deployed.prefab'] = 'box.wooden'
    Data['large_woodbox_deployed.prefab'] = 'box.wooden.large'
    Data['campfire_deployed.prefab'] = 'campfire'
    Data['crudeoutput.prefab'] = 'mining.pumpjack'
    Data['hopperoutput.prefab'] = 'mining.guarry'
    Data['cupboard.tool.deployed.prefab'] = 'cupboard.tool'
    Data['furnace_deployed.prefab'] = 'furnace'
    Data['lantern_deployed.prefab'] = 'lantern'
    Data['large_furnace_deployed.prefab'] = 'large.furnace'
    Data['repairbench_deployed.prefab'] = 'box_repair.bench'
    Data['researchtable_deployed.prefab'] = 'research.table'
    Data['sign.huge.wood.prefab'] = 'sign.wooden.huge'
    Data['sign.large.wood.prefab'] = 'sign.wooden.large'
    Data['sign.medium.wood.prefab'] = 'sign.wooden.medium'
    Data['sign.small.wood.prefab'] = 'sign.wooden.small'
    Data['sleepingbag_leather_deployed.prefab'] = 'sleepingbag'
    Data['refinery_small_deployed.prefab'] = 'small.oil.refinery'
    Data['beartrap.prefab'] = 'trap.bear'
    Data['landmine.prefab'] = 'trap.landmine'
    Data['floor_spikes.prefab'] = 'spikes.floor'
    Data['water_catcher_large.prefab'] = 'water.catcher.large'
    Data['water_catcher_small.prefab'] = 'water.catcher.small'

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
                                name = CombatEntityHurtEvent.Victim.baseEntity.LookupShortPrefabName().replace('_', '.')
                                name = name.replace('.deployed', '')
                                name = name.replace('.prefab', '')
                                item = ItemManager.FindItemDefinition(name)
                                Player.Inventory.Add(item.itemid, 1)
                                Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                            except:
                                try:
                                    #Backup, Checks dictionary if above fails
                                    item = ItemManager.FindItemDefinition(self.Data[CombatEntityHurtEvent.Victim.baseEntity.LookupShortPrefabName()])
                                    if item is not None:
                                        Player.Inventory.Add(item.itemid, 1)
                                        Util.DestroyEntity(CombatEntityHurtEvent.Victim.baseEntity)
                                    else:
                                        Player.Message("You can not remove this item!")
                                except:
                                    Player.Message("You can not remove this item!")
                        return
                    else:
                        Player.MessageFrom("RemoveTool", DataStore.Get("RemoveTool", "OFR"))
        return
        
