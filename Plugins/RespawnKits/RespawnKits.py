__title__ = 'RespawnKits'
__author__ = 'Jakkee'
__about__ = 'Get a kit on respawn!'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton

 
class RespawnKits:
    def On_PluginInit(self):
        if not Plugin.IniExists("RespawnKit"):
            Plugin.CreateIni("RespawnKit")
            ini = Plugin.GetIni("RespawnKit")
            ini.AddSetting("PlayerKit", "Wear0", "Boonie Hat, 1")
            ini.AddSetting("PlayerKit", "Wear1", "Hoodie, 1")
            ini.AddSetting("PlayerKit", "Wear2", "Metal Chest Plate, 1")
            ini.AddSetting("PlayerKit", "Wear3", "Leather Gloves, 1")
            ini.AddSetting("PlayerKit", "Wear4", "Pants, 1")
            ini.AddSetting("PlayerKit", "Wear5", "Boots, 1")
            ini.AddSetting("PlayerKit", "Belt0", "Assault Rifle, 1")
            ini.AddSetting("PlayerKit", "Belt1", "Custom SMG, 1")
            ini.AddSetting("PlayerKit", "Belt2", "Medical Syringe, 1")
            ini.AddSetting("PlayerKit", "Belt3", "Cooked Wolf Meat, 20")
            ini.AddSetting("PlayerKit", "Belt4", "Hatchet, 1")
            ini.AddSetting("PlayerKit", "Belt5", "Pick Axe, 1")
            ini.AddSetting("PlayerKit", "Main0", "5.56 Rifle Ammo, 64")
            ini.AddSetting("PlayerKit", "Main1", "5.56 Rifle Ammo, 64")
            ini.AddSetting("PlayerKit", "Main2", "Pistol Bullet, 64")
            ini.AddSetting("PlayerKit", "Main3", "Pistol Bullet, 64")
            ini.AddSetting("PlayerKit", "Main4", "Medical Syringe, 1")
            ini.Save()
        ini = Plugin.GetIni("RespawnKit")
        DataStore.Flush("PlayerKit")
        for slot in ini.EnumSection("PlayerKit"):
            DataStore.Add("PlayerKit", slot, ini.GetSetting("PlayerKit", slot))

    def On_PlayerWakeUp(self, Player):
        if len(Player.Inventory.AllItems()) == 2:
            for item in Player.Inventory.AllItems():
                item._item.RemoveFromContainer()
            for slot in DataStore.Keys("PlayerKit"):
                if slot[:-1] == "Wear":
                    item = DataStore.Get("PlayerKit", slot).split(",")
                    Player.Inventory.InnerWear.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                elif slot[:-1] == "Belt":
                    item = DataStore.Get("PlayerKit", slot).split(",")
                    Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))
                else:
                    item = DataStore.Get("PlayerKit", slot).split(",")
                    Player.Inventory.InnerMain.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1][1:]))

    def Tryint(self, Arg):
        try:
            number = int(Arg)
            return number
        except:
            return 1
