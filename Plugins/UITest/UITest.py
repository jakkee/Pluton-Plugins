import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton


 
class UITest:
    def On_PluginInit(self):
        Commands.Register("makeui")\
            .setCallback("makeui")\
            .setDescription("Creates a test UI")\
            .setUsage("/makeui")
        
    def makeui(self, args, Player):
        commui = Pluton.PlutonUIEntity(Player.basePlayer.net.connection)
        testpanel7766 = commui.AddPanel("TestPanel7766", "Overlay")
        testpanel7766.AddComponent<Pluton.PlutonUI.NeedsCursor>()
        testpanel7766.AddComponent(Pluton.PlutonUI.RectTransform(
            anchormin = "0 0",
            anchormax = "1 1"))
        testpanel7766.AddComponent(Pluton.PlutonUI.RawImage(
            color = "1.0 1.0 1.0 1.0",
            url = "http://files.facepunch.com/garry/2015/June/03/2015-06-03_12-19-17.jpg"))
        nonamepanel = commui.AddPanel(None, "TestPanel7766");
        nonamepanel.AddComponent(Pluton.PlutonUI.Text(
            text = "Do you want to press a button?",
            fontSize = 32, align = "MiddleCenter"))
        nonamepanel.AddComponent(Pluton.PlutonUI.RectTransform(
            anchormin = "0 0.5",
            anchormax = "1 0.9"))
        Button88 = commui.AddPanel("Button88", "TestPanel7766")
        Button88.AddComponent(Pluton.PlutonUI.Button(
            close = "TestPanel7766",
            command = "status",
            color = "0.9 0.8 0.3 0.8",
            imagetype = "Tiled"))
        Button88.AddComponent(Pluton.PlutonUI.RectTransform(
            anchormin = "0.3 0.15",
            anchormax = "0.7 0.2"))
        nn2 = commui.AddPanel(None, "Button88");
        nn2.AddComponent(Pluton.PlutonUI.Text(
            text = "YES",
            fontSize = 20,
            align = "MiddleCenter"))
        commui.CreateUI()
        
