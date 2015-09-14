__title__ = 'EasySpectate'
__author__ = 'Jakkee'
__about__ = 'Easily EasySpectate players'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton

 
class EasySpectate:   
    def On_PluginInit(self):
        Commands.Register("spectate").setCallback("spectate").setDescription("enter spetcate mode").setUsage("/spectate")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "Owner can use", "True")
            ini.AddSetting("Settings", "Admins can use", "True")
            ini.AddSetting("Settings", "Moderators can use", "True")
            ini.AddSetting("Settings", "Players can use", "False")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("Spectate")
        DataStore.Add("Spectate", "Owner", ini.GetBoolSetting("Settings", "Owner can use"))
        DataStore.Add("Spectate", "Admin", ini.GetBoolSetting("Settings", "Admins can use"))
        DataStore.Add("Spectate", "Moderator", ini.GetBoolSetting("Settings", "Moderators can use"))
        DataStore.Add("Spectate", "Players", ini.GetBoolSetting("Settings", "Players can use"))

    def Tryint(self, Arg):
        try:
            number = int(Arg)
            return number
        except:
            return 1

    def canuse(self, Player):
        if Player.Owner:
            if DataStore.Get("Spectate", "Owner"):
                return True
            else:
                return False
        elif Player.Admin:
            if DataStore.Get("Spectate", "Admin"):
                return True
            else:
                return False
        elif Player.Moderator:
            if DataStore.Get("Spectate", "Moderator"):
                return True
            else:
                return False
        else:
            if DataStore.Get("Spectate", "Players"):
                return True
            else:
                return False

    def saveinv(self, Player):
        count = 0
        for item in Player.Inventory.WearItems():
            DataStore.Add("SpectateData:" + Player.SteamID, "Wear" + str(count), item.Name + "," + str(item.Amount))
            count += 1
        count = 0
        for item in Player.Inventory.BeltItems():
            DataStore.Add("SpectateData:" + Player.SteamID, "Belt" + str(count), item.Name + "," + str(item.Amount))
            count += 1
        count = 0
        for item in Player.Inventory.MainItems():
            DataStore.Add("SpectateData:" + Player.SteamID, "Main" + str(count), item.Name + "," + str(item.Amount))
            count += 1

    def giveinv(self, Player):
        if len(Player.Inventory.AllItems()) == 2:
            for item in Player.Inventory.AllItems():
                item._item.RemoveFromContainer()
            for slot in DataStore.Keys("SpectateData:" + Player.SteamID):
                if slot[:-1] == "Wear":
                    item = DataStore.Get("SpectateData:" + Player.SteamID, slot).split(",")
                    Player.Inventory.InnerWear.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1]))
                elif slot[:-1] == "Belt":
                    item = DataStore.Get("SpectateData:" + Player.SteamID, slot).split(",")
                    Player.Inventory.InnerBelt.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1]))
                else:
                    item = DataStore.Get("SpectateData:" + Player.SteamID, slot).split(",")
                    Player.Inventory.InnerMain.AddItem(Find.ItemDefinition(item[0]), self.Tryint(item[1]))
            Player.Message("You have received your items back!")

    def spectate(self, args, Player):
        if self.canuse(Player):
            if Player.basePlayer.IsSpectating():
                Player.basePlayer.StopSpectating()
                self.giveinv(Player)
                DataStore.Flush("SpectateData:" + Player.SteamID)
                Player.Message("You are no longer spectating!")
            else:
                self.saveinv(Player)
                Player.basePlayer.StartSpectating()
        else:
            Player.Message("You are not allowed to use this command!")

    def On_PlayerHurt(self, PlayerHurtEvent):
        if PlayerHurtEvent.Victim.basePlayer.IsSpectating():
            for x in range(0, len(CombatEntityHurtEvent.DamageAmounts)):
                CombatEntityHurtEvent.DamageAmounts[x] = 0
            if PlayerHurtEvent.Attacker.IsPlayer():
                PlayerHurtEvent.Attacker.ToPlayer().Message(PlayerHurtEvent.Victim.Name + " is currently spectating and can not take damage!")
            else:
                return
            
                
