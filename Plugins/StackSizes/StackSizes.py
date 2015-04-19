__title__ = 'StackSizes'
__author__ = 'Jakkee'
__version__ = '1.0.3'

import clr
clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
import ItemDefinition
import ItemManager
import Pluton


class StackSizes:
    def On_PluginInit(self):
        if not Plugin.IniExists("ItemsList"):
            Util.Log("------- StackSizes -------")
            Util.Log("Creating new ini File...")
            Plugin.CreateIni("ItemsList")
            ini = Plugin.GetIni("ItemsList")
            items = ItemManager.GetItemDefinitions()
            for item in items:
                ini.AddSetting("StackSizes", item.shortname, str(item.stackable))
                ini.Save()
            Util.Log("Done")
            Util.Log("--------------------------")
        ini = Plugin.GetIni("ItemsList")
        Util.Log("------- StackSizes -------")
        Util.Log("Searching for new items...")
        count = 0
        for item in ItemManager.GetItemDefinitions():
            if ini.GetSetting("StackSizes", item.shortname) == "":
                ini.AddSetting("StackSizes", item.shortname, str(item.stackable))
                ini.Save()
                count += 1
        if count > 0:
            Util.Log("Found " + str(count) + " new items...")
            Util.Log("Adding them to the list...")
            Util.Log("Done.")
            Util.Log("--------------------------")
        else:
            Util.Log("Found 0 new items...")
            Util.Log("Done.")
            Util.Log("--------------------------")
        for key in ini.EnumSection("StackSizes"):
            if ItemManager.FindItemDefinition(key) == None:
                Util.Log("Could not set stack size for: " + key)
                continue
            ItemManager.FindItemDefinition(key).stackable = int(ini.GetSetting("StackSizes", key))
