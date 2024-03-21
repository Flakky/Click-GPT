import os
import threading
import pystray
from PIL import Image, ImageDraw

class Tray:
    icon:pystray.Icon
    exit_call = None

    def __init__(self) -> None:
        self.icon: pystray.Icon = None
        pass


    def exit(self):
        self.icon.stop()
        self.exit_call()


    def init_tray_icon(self, exit_call):

        self.exit_call = exit_call

        script_path = os.path.dirname(__file__)
           
        image = Image.open(os.path.join(script_path, '../res/icon.png'))

        menu = (pystray.MenuItem("Exit", self.exit),)

        self.icon = pystray.Icon('ClickGPT', image, 'ClickGPT', menu)

        return
    
    def start(self):
        thread = threading.Thread(target=self.icon.run)
        thread.daemon = True
        thread.start()

