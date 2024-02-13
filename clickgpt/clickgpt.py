import pyperclip
import time
import keyboard
import pygetwindow as gw
import pyautogui
import contextwindow
import gpt

class ClickGPTContext:
    aiclient: gpt.OpenAI
    options:dict[str, contextwindow.TextOption]

    def __init__(self, aiclient:gpt.OpenAI, options:dict[str, contextwindow.TextOption]) -> None:
        self.aiclient = aiclient
        self.options = options
        

class SendTextContext:
    window: contextwindow = None
    aiclient = None

    def __init__(self, window:contextwindow, aiclient) -> None:
        self.window = window
        self.aiclient = aiclient
        

def send_option_request(request:str, context:SendTextContext):
    open_ai_request = gpt.OpenAITextRequest(context.aiclient, request)
    response = gpt.text_request(open_ai_request)
    context.window.set_response_text(response)


def on_hotkey(gpt_context: ClickGPTContext):
    window = contextwindow.ContextWindow()
    context = SendTextContext(window, gpt_context.aiclient)
    option_callback = lambda tag, option: (
        print(tag),
        send_option_request(option.request.format(text=window.get_request_text()), context)
    )
    
    window.create(gpt_context.options, option_callback)

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
    

def init(context: ClickGPTContext):
    keyboard.add_hotkey('ctrl+`', lambda: on_hotkey(context))
    input("Press Enter to quit") 


