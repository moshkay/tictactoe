from kivy.atlas import Atlas
import os
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_string("""
<Label>:
    canvas.before:
        Rectangle:
            pos:self.pos
            size:self.size
            source:"atlas://c:/python34/tictactoe/tictactoe_project/images/tictactoe/splash"




""")


##Atlas.create(outname="tictactoe",
##             filenames=["o.jpg",
##                        "x.jpg",
##                        "playerx.jpg",
##                        "playero.jpg",
##                        "splash.jpg",
##                        "icon.jpg",
##                        "p2p.jpg",
##                        "p2c.jpg",
##                        "back.jpg"],
##             size=[1200,800],
##             use_path=False,padding=3)
##path=os.getcwd()
##v=Atlas("c:\\python34\\tictactoe\\tictactoe project\\tictactoe.atlas")
##for i in v.textures():
##    print(i)

class Interface(FloatLayout):
    def __init__(self,**opt):
        super().__init__(**opt)
        label=Label(text="my label")
        self.add_widget(label)
runTouchApp(Interface())
