import clickgpt
import configparser
import gpt
import os
import sys
import settings

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

   clickgpt.init(gpt_client)