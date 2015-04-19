__title__ = 'Shop'
__author__ = 'Jakkee'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Pluton")
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
        args = cmd.args
        if cmd.cmd == "shop":
            if len(args) == 1:
                if args[0] == "lookup":
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection("Categories")
                    for x in keys:
                        Player.MessageFrom("Shop", x)
                elif args[0] == "buy":
                    Player.MessageFrom("Shop", "Usage: /shop buy [item] [amount]")
                elif args[0] == "sell":
                    Player.MessageFrom("Shop", "Usage: /shop sell [item] [amount]")
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category] - Lists items in a category")
            elif len(args) == 2:
                if args[0] == "lookup":
                    ini = Plugin.GetIni("Settings")
                    keys = ini.EnumSection(args[1])
                    for x in keys:
                        buy = float(ini.GetSetting(args[1], x))
                        percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                        percentoff = (buy * percent)
                        sell = (buy - percentoff)
                        Player.MessageFrom("Shop - " + args[1], x + "  [Buy: " + DataStore.Get("iConomy", "MoneyMark") + str(buy) + ": Sell: " + DataStore.Get("iConomy", "MoneyMark") + str(sell) + "]")
                        #Player.MessageFrom("Shop - " + args[1], x + "  [Buy: " + DataStore.Get("iConomy", "MoneyMark") + str(buy) + "]")
                elif args[0] == "buy":
                    Player.MessageFrom("Shop", "Usage: /shop buy [item] [amount]")
                elif args[0] == "sell":
                    Player.MessageFrom("Shop", "Usage: /shop sell [item] [amount]")
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category] - Lists items in a category")
            elif len(args) == 3:
                if args[0] == "buy":
                    oitem = args[1]
                    amount = self.intcheck(args[2])
                    if amount is None:
                        Player.MessageFrom("Shop", "The amount you have entered is not a number!")
                        return
                    try:
                        item = Find.ItemDefinition(oitem).shortname
                        ini = Plugin.GetIni("Settings")
                        keys = ini.EnumSection("Categories")
                        price = -0
                        for x in keys:
                            if ini.GetSetting(x, item) is not None:
                                price = self.intcheck(ini.GetSetting(x, oitem))
                                break
                        if not price == -0:
                            price = (price * amount)
                            costs = float(DataStore.Get("iConomy", Player.SteamID)) - price
                            if not costs < 0.0:
                                DataStore.Add("iConomy", Player.SteamID, costs)
                                Player.Inventory.Add(item, amount)
                                Player.MessageFrom("Shop", "You have brought " + str(amount) + "x " + item + " for " + DataStore.Get("iConomy", "MoneyMark") + str(price))
                            else:
                                Player.MessageFrom("Shop", "You do not have enough money to buy " + str(amount) + "x " + item)
                        else:
                            Player.MessageFrom("Shop", "Can not find: " + oitem)
                    except:
                        Player.MessageFrom("Shop", "Can not find: " + oitem)
                elif args[0] == "sell":
                    oitem = args[1]
                    amount = self.intcheck(args[2])
                    if amount is None:
                        Player.MessageFrom("Shop", "The amount you have entered is not a number!")
                        return
                    try:
                        item = Find.ItemDefinition(oitem).shortname
                        ini = Plugin.GetIni("Settings")
                        keys = ini.EnumSection("Categories")
                        price = None
                        for x in keys:
                            if ini.GetSetting(x, item) is not None:
                                price = ini.GetSetting(x, oitem)
                        if price is not None:
                            percent = float(ini.GetSetting("Settings", "SellPercentage").Replace("%", "")) / 100
                            percentoff = (float(price) * percent)
                            costs = (float(price) - percentoff)
                            enough = None
                            for x in Player.Inventory.AllItems():
                                invitem = x._item.info.shortname
                                Player.Message(invitem)
                                if invitem == item:
                                    if x.Amount >= int(amount):
                                        enough = "yes"
                                        break
                                    else:
                                        break
                            if enough == "yes":
                                count = 0
                                for x in Player.Inventory.AllItems():
                                    if x._item.info.shortname == item:
                                        x._item.condition = float(0)
                                        count += 1
                                        if count == int(amount):
                                            DataStore.Add("iConomy", Player.SteamID, float(DataStore.Get("iConomy", Player.SteamID)) + costs)
                                            Player.MessageFrom("Shop", "You have sold " + str(amount) + "x " + item + " for " + DataStore.Get("iConomy", "MoneyMark") + price)
                                            break
                        else:
                            Player.MessageFrom("Shop", "Can not find: " + oitem)
                    except:
                        Player.MessageFrom("Shop", "Can not find: " + oitem)
                elif args[0] == "lookup":
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category] - Lists items in a category")
                else:
                    Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                    Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                    Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                    Player.MessageFrom("Shop", "/shop lookup [category] - Lists items in a category")
            else:
                Player.MessageFrom("Shop", "/shop buy [item] [amount] - Buy an item")
                Player.MessageFrom("Shop", "/shop sell [item] [amount] - Sell an item")
                Player.MessageFrom("Shop", "/shop lookup - Lists categories")
                Player.MessageFrom("Shop", "/shop lookup [category] - Lists items in a category")
