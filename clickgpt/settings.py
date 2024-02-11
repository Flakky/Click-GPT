import os

def add_to_startup():
    #TODO: add other Linux + Mac
    file_path = os.path.dirname(os.path.realpath(__file__))

    with open(get_startup_file_path_win(), "w+") as bat_file:
        bat_file.write(f'python {file_path}')

    print('ClickGPT added to startup')

def remove_from_startup():
    #TODO: add other Linux + Mac
    file_path = get_startup_file_path_win()
    if os.path.isfile(file_path):
        os.remove(file_path)
        print('ClickGPT removed from startup')

def get_startup_file_path_win():
    print(os.getenv('APPDATA'))
    return os.path.join(os.getenv('APPDATA'), 'Microsoft/Windows/Start Menu/Programs/Startup/ClickGPT.bat')