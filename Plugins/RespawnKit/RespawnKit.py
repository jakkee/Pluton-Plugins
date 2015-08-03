__title__ = 'RespawnKit'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


class RespawnKit:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "AdminKit", "PlayerRespawnKit")
            ini.AddSetting("Settings", "PlayerKit", "PlayerRespawnKit")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("RespawnKit")
        DataStore.Add("RespawnKit", "Admin", ini.GetSetting("Settings", "AdminKit"))
        DataStore.Add("RespawnKit", "Player", ini.GetSetting("Settings", "PlayerKit"))
        Server.LoadLoadouts()

    def On_PlayerWakeUp(Self, Player):
        if len(Player.Inventory.AllItems()) == 2:
            count = 0
            for item in Player.Inventory.AllItems():
                if item.Name == "Rock":
                    count += 1
                elif item.Name == "Torch":
                    count += 1
            if count == 2:
                for item in Player.Inventory.AllItems():
                    Player.Inventory._inv.Take(Player.Inventory._inv.FindItemIDs(item.ItemID), item.ItemID, 1)
            if Player.Admin:
                kit = DataStore.Get("RespawnKit", "Admin")
                #try:
                Server.LoadOuts.ContainsKey(kit)
                loadout = Server.LoadOuts[kit]
                loadout.ToInv(Player.Inventory)
                #except:
                    #Util.Log("RespawnKit: No admin kit called: " + kit)
                    #Player.Inventory.Add(3506021)
                    #Player.Inventory.Add(110547964)
            else:
                kit = DataStore.Get("RespawnKit", "Player")
                try:
                    Server.LoadOuts.ContainsKey(kit)
                    loadout = Server.LoadOuts[kit]
                    loadout.ToInv(Player.Inventory)
                except:
                    Util.Log("RespawnKit: No player kit called: " + kit)
                    Player.Inventory.Add(3506021)
                    Player.Inventory.Add(110547964)
        else:
            return
