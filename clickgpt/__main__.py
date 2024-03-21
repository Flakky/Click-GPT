import clickgpt
import configparser
import gpt
import os
import sys
import settings
import json
import contextwindow
from tray import Tray

if __name__ == "__main__":
   config = configparser.ConfigParser()
   config.sections()

   script_path = os.path.dirname(__file__)

   config_path = script_path+'/../config.ini'
   print(config_path)

   config.read(config_path)
   api_key = config.get("OpenAI", "ApiKey")

   startup = config.get("Settings", "LaunchAtStartup")
   if(startup): settings.add_to_startup()
   else: settings.remove_from_startup()

   gpt_client = gpt.create_client(api_key)

   options_obj: dict = {}
   with open(os.path.join(script_path, '../options.json'), 'r') as file:
      options_obj = json.load(file)

   options: dict[str: contextwindow.TextOption] = {}
   for (key, val) in options_obj.items():
      options[key] = contextwindow.TextOption.from_dict(val)

   clickgptcontext = clickgpt.ClickGPTContext(gpt_client, options)

   cgpt = clickgpt.ClickGPT()

   tray = Tray()
   tray.init_tray_icon(cgpt.exit)
   tray.start()

   cgpt.init(clickgptcontext)