import pyperclip
import time
import keyboard
import pygetwindow as gw
import pyautogui
import contextwindow
import gpt


# TODO: Move to config or something
options = {
    "fix_grammar": {"name": "Fix grammar", "request": "Fix grammar of the given text. Do not print anything except fixed text: {text}"},
    "improve_text": {"name": "Improve text", "request": "Improve given text. Do not print anything except improved text: {text}"},
}

class SendTextContext:
    window: contextwindow = None
    aiclient = None

    def __init__(self, window:contextwindow, aiclient) -> None:
        self.window = window
        self.aiclient = aiclient
        

def send_option_request(tag:str, context:SendTextContext):
    open_ai_request = gpt.OpenAITextRequest(context.aiclient, options[tag]["request"].format(text=context.window.get_request_text()))
    response = gpt.text_request(open_ai_request)
    context.window.set_response_text(response)


def on_hotkey(aiclient):
    select_options = []

    for tag, option in options.items():
        select_options.append(contextwindow.TextOption(tag, option["name"]))

    window = contextwindow.ContextWindow()
    context = SendTextContext(window, aiclient)
    option_callback = lambda tag: send_option_request(tag, context)
    window.create(select_options, option_callback)

    selected_text = copy_selected_text()
    print(selected_text)
    window.set_request_text(selected_text)

    window.show()


def copy_selected_text():
    active_window = gw.getActiveWindow()
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            print(f"Active window: {active_window.title}")
            active_window.activate()
            print(f"Copy text")
            pyautogui.keyUp('ctrl') # just to make sure button C will not treated as a simple command after hotkey
            time.sleep(0.1)
            pyautogui.keyDown('ctrl')
            time.sleep(0.1)
            pyautogui.keyDown('c')
            time.sleep(0.1)
            pyautogui.keyUp('c')
            time.sleep(0.1)
            pyautogui.keyUp('ctrl')

            # time.sleep(0.1)  # Wait a bit for the copy command to execute
            text = pyperclip.paste()
            print(f"Return selected text {text}")

            return text
        else:
            print("No active window detected.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def init(aiclient):
    keyboard.add_hotkey('ctrl+`', lambda: on_hotkey(aiclient))  
    input("Press Enter to quit") 


