__title__ = 'AntiTowerRaid'
__author__ = 'Jakkee'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import UnityEngine
import BaseEntityEx

 
class AntiTowerRaid:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Max blocks stacked", "3")
            ini.AddSetting("Config", "Destroy Message", "You are not allowed to stack these this high!")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("AntiTowerRaid", "Stack", ini.GetSetting("Config", "Max blocks stacked"))
        DataStore.Add("AntiTowerRaid", "Message", ini.GetSetting("Config", "Destroy Message"))

    def On_Placement(self, BuildingEvent):        
        if BuildingEvent.BuildingPart.Name == "build/block.halfheight":
            Player = BuildingEvent.Builder
            count = 0
            loc = BuildingEvent.BuildingPart.Location
            down = BuildingEvent.BuildingPart.Location.down
            hit = UnityEngine.Physics.RaycastAll(loc, down)
            for x in hit:
                entity = UnityEngine.BaseEntityEx.ToBaseEntity(x.collider.gameObject)
                if entity is not None:
                    if entity.name == "build/block.halfheight":
                        count += 1
                        Player.Message(str(count))
                        if count > int(DataStore.Get("AntiTowerRaid", "Stack")):
                            Player.MessageFrom("AntiTowerRaid", DataStore.Get("AntiTowerRaid", "Message"))
                            Util.DestroyEntity(entity)
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            
