__title__ = 'Shop'
__author__ = 'Jakkee'
__about__ = 'Buy/Sell items'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton", "Assembly-CSharp")
import ItemManager
import Pluton

 
class Shop:
    def intcheck(self, i):
        try:
            i = int(i)
            if i > 0:
                return i
            else:
                return 1
        except:
            return None
        
    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        if cmd.cmd == "shop" or cmd.cmd == "s":
            if len(args) == 1:
                if args[0] == "lookup" or args[0] == "l":
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    for x in keys:
                        Player.MessageFrom("Shop", x)
                elif args[0] == "buy" or args[0] == "b":
                    Player.MessageFrom("Shop", "Usage: /shop buy [item] [amount]")
                elif args[0] == "sell" or args[0] == "s":
                    Player.MessageFrom("Shop", "Usage: /shop sell [item] [amount]")
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category/item] - Lists items buy / sell prices")
            elif len(args) == 2:
                if args[0] == "lookup" or args[0] == "l":
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection(args[1])
                    count = 0
                    for x in keys:
                        item = ItemManager.FindItemDefinition(x)
                        if item is not None:
                            buy = float(ini.GetSetting(args[1], x))
                            percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                            percentoff = (buy * percent)
                            sell = (buy - percentoff)
                            Player.MessageFrom("Shop - " + args[1], item.shortname + " [Buy: " + DataStore.Get("iConomy", "MoneyMark") + str(buy) + ": Sell: " + DataStore.Get("iConomy", "MoneyMark") + str(sell) + "]")
                            count += 1
                        else:
                            continue
                    if count == 0:
                        item = ItemManager.FindItemDefinition(args[1])
                        if item is None:
                            Player.MessageFrom("Shop", "Could not find category or an item with that name!")
                            return
                        ini = Plugin.GetIni("Settings")
                        keys = ini.EnumSection("Categories")
                        price = None
                        for x in keys:
                            if not ini.GetSetting(x, item.shortname) == "":
                                price = self.intcheck(ini.GetSetting(x, item.shortname))
                                if price is not None:
                                    buy = float(ini.GetSetting(x, item.shortname))
                                    percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                                    percentoff = (buy * percent)
                                    sell = (buy - percentoff)
                                    Player.MessageFrom("Shop - Lookup", item.shortname + "  [Buy: " + DataStore.Get("iConomy", "MoneyMark") + str(buy) + ": Sell: " + DataStore.Get("iConomy", "MoneyMark") + str(sell) + "]")
                                    break
                                else:
                                    Player.MessageFrom("Shop", "Shop does not buy or sell this item!")
                                    break
                    else:
                        return
                elif args[0] == "buy" or args[0] == "b":
                    oitem = args[1]
                    amount = 1
                    item = ItemManager.FindItemDefinition(oitem)
                    if item is None:
                        Player.MessageFrom("Shop", "Can not find: " + oitem + ". You have to use a shortname!")
                        return
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    price = None
                    for x in keys:
                        if not ini.GetSetting(x, item.shortname) == "":
                            price = self.intcheck(ini.GetSetting(x, item.shortname))
                    if price is not None:
                        price = (price * amount)
                        costs = float(DataStore.Get("iConomy", Player.SteamID)) - price
                        if not costs < 0.0:
                            DataStore.Add("iConomy", Player.SteamID, costs)
                            Player.Inventory.Add(item.itemid, amount)
                            Player.MessageFrom("Shop", "You have brought " + str(amount) + " x " + item.shortname + " for " + DataStore.Get("iConomy", "MoneyMark") + str(price))
                        else:
                            Player.MessageFrom("Shop", "You do not have enough money to buy " + str(amount) + " x " + item.shortname)
                    else:
                        Player.MessageFrom("Shop", "The shop does not sell: " + item.shortname)
                elif args[0] == "sell" or args[0] == "s":
                    oitem = args[1]
                    amount = 1
                    item = ItemManager.FindItemDefinition(oitem)
                    if item is None:
                        Player.MessageFrom("Shop", "Can not find: " + oitem + ". You have to use a shortname!")
                        return
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    price = None
                    for x in keys:
                        if not ini.GetSetting(x, item.shortname) == "":
                            price = self.intcheck(ini.GetSetting(x, item.shortname))
                    if price is not None:
                        playerAmount = Player.Inventory._inv.GetAmount(item.itemid)
                        if playerAmount >= amount:
                            percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                            percentoff = float(price) * percent
                            costs = (float(price) - percentoff) * float(amount)
                            Player.Inventory._inv.Take(Player.Inventory._inv.FindItemIDs(item.itemid), item.itemid, amount)
                            DataStore.Add("iConomy", Player.SteamID, float(DataStore.Get("iConomy", Player.SteamID)) + costs)
                            Player.MessageFrom("Shop", "You have sold " + item.shortname + " x " + str(amount) + " for " + DataStore.Get("iConomy", "MoneyMark") + str(costs))
                            Player.Inventory.Notice(" + " + str(costs))
                        else:
                            Player.MessageFrom("Shop", "You do not have " + str(amount) + " x " + item.shortname + " to sell!")
                    else:
                        Player.MessageFrom("Shop", "The shop does not buy: " + item.shortname)
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category/item] - Lists items buy / sell prices")
            elif len(args) == 3:
                if args[0] == "buy" or args[0] == "b":
                    oitem = args[1]
                    amount = self.intcheck(args[2])
                    if amount is None:
                        Player.MessageFrom("Shop", "The amount you have entered is not a number!")
                        return
                    item = ItemManager.FindItemDefinition(oitem)
                    if item is None:
                        Player.MessageFrom("Shop", "Can not find: " + oitem + ". You have to use a shortname!")
                        return
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    price = None
                    for x in keys:
                        if not ini.GetSetting(x, item.shortname) == "":
                            price = self.intcheck(ini.GetSetting(x, item.shortname))
                    if price is not None:
                        price = (price * amount)
                        costs = float(DataStore.Get("iConomy", Player.SteamID)) - price
                        if not costs < 0.0:
                            DataStore.Add("iConomy", Player.SteamID, costs)
                            Player.Inventory.Add(item.itemid, amount)
                            Player.MessageFrom("Shop", "You have brought " + str(amount) + " x " + item.shortname + " for " + DataStore.Get("iConomy", "MoneyMark") + str(price))
                        else:
                            Player.MessageFrom("Shop", "You do not have enough money to buy " + str(amount) + " x " + item.shortname)
                    else:
                        Player.MessageFrom("Shop", "The shop does not sell: " + item.shortname)
                elif args[0] == "sell" or args[0] == "s":
                    oitem = args[1]
                    amount = self.intcheck(args[2])
                    if amount is None:
                        Player.MessageFrom("Shop", "The amount you have entered is not a number!")
                        return
                    item = ItemManager.FindItemDefinition(oitem)
                    if item is None:
                        Player.MessageFrom("Shop", "Can not find: " + oitem + ". You have to use a shortname!")
                        return
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    price = None
                    for x in keys:
                        if not ini.GetSetting(x, item.shortname) == "":
                            price = self.intcheck(ini.GetSetting(x, item.shortname))
                    if price is not None:
                        playerAmount = Player.Inventory._inv.GetAmount(item.itemid)
                        if playerAmount >= amount:
                            percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                            percentoff = float(price) * percent
                            costs = (float(price) - percentoff) * float(amount)
                            Player.Inventory._inv.Take(Player.Inventory._inv.FindItemIDs(item.itemid), item.itemid, amount)
                            DataStore.Add("iConomy", Player.SteamID, float(DataStore.Get("iConomy", Player.SteamID)) + costs)
                            Player.MessageFrom("Shop", "You have sold " + item.shortname + " x " + str(amount) + " for " + DataStore.Get("iConomy", "MoneyMark") + str(costs))
                            Player.Inventory.Notice(" + " + str(costs))
                        else:
                            Player.MessageFrom("Shop", "You do not have " + str(amount) + " x " + item.shortname + " to sell!")
                    else:
                        Player.MessageFrom("Shop", "The shop does not buy: " + item.shortname)
                elif args[0] == "lookup" or args[0] == "l":
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category/item] - Lists items buy / sell prices")
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category/item] - Lists items buy / sell prices")
            else:
                Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                Player.MessageFrom("Shop", "/shop lookup [category/item] - Lists items buy / sell prices")
