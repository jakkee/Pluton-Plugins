__title__ = 'CreativeServer'
__author__ = 'Jakkee'
__about__ = 'Upgrade building blocks'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton", "UnityEngine", "Assembly-CSharp")
import Pluton
import UnityEngine
import BuildingBlock


grades = {'Twigs': 0,\
          'Wood': 1,\
          'Stone': 2,\
          'Metal': 3,\
          'TopTier': 4}

lolgrades = {0: "Twigs",\
             1: "Wood",\
             2: "Stone",\
             3: "Metal",\
             4: "TopTier"}
 
class CreativeServer:    
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Crafting Costs Nothing", "True")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("BuildingUpgrades", "Craft", ini.GetSetting("Config", "Crafting Costs Nothing"))

    def On_Command(self, CommandEvent):
        cmd = CommandEvent.cmd
        Player = CommandEvent.User
        args = CommandEvent.args
        if cmd == "up":
            building_Block = Player.GetLookBuildingPart(float(100))
            if building_Block == None:
                Player.Message("You are not looking at a building block!")
                return
            else:
                lol = ""
                hit = UnityEngine.Physics.OverlapSphere(building_Block.buildingBlock.transform.position, float(3.5))
                for block in hit:
                    entity = UnityEngine.BaseEntityEx.ToBaseEntity(block.gameObject)
                    if entity is not None:
                        hit = UnityEngine.Physics.OverlapSphere(entity.transform.position, float(3.5))
                        lol = lol + entity + ","
                count = lol.split(',')
                count = str(len(lol))
                Player.Message(count)
                """
                try:
                    entity = UnityEngine.BaseEntityEx.ToBaseEntity(entity.gameObject)
                    #Player.Message(str(entity.grade))
                    if not grades[str(entity.grade)] > 4 :
                        #entity.grade = entity.currentGrade.gradeBase.type + 1
                        entity.SetHealthToMax()
                        entity.SendNetworkUpdate(Player.basePlayer.NetworkQueue.Update)
                except:
                    pass
                    """
            
