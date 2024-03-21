import pyperclip
import time
import keyboard
import pygetwindow as gw
import pyautogui
import contextwindow
import gpt
import tkinter as tk
import ttkbootstrap as ttk
import sys


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

class ClickGPT:
    context_window: contextwindow.ContextWindow
    tkroot: tk.Tk

    def __init__(self) -> None:
        self.context_window = None
        pass

    def send_option_request(self, request:str, context:SendTextContext):
        open_ai_request = gpt.OpenAITextRequest(context.aiclient, request)
        response = gpt.text_request(open_ai_request)
        context.window.set_response_text(response)


    def on_hotkey(self, gpt_context: ClickGPTContext):
        print('Hot key pressed')

        selected_text = self.copy_selected_text()
        print(selected_text)

    #    if gpt_context.context_window is None:
        gpt_context.context_window = contextwindow.ContextWindow()
        context = SendTextContext(gpt_context.context_window, gpt_context.aiclient)
        option_callback = lambda tag, option: (
            print(tag),
            self.send_option_request(option.request.format(text=gpt_context.context_window.get_request_text()), context)
        )

        gpt_context.context_window.create(gpt_context.options, option_callback)
        gpt_context.context_window.set_request_text(selected_text)

    def copy_selected_text(self):
        active_window = gw.getActiveWindow()
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                print(f"Active window: {active_window.title}")
                active_window.activate()
                print(f"Copy text")
                pyautogui.keyUp('ctrl') # just to make sure button C will not treated as a simple command after hotkey
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('c')
                pyautogui.keyUp('c')
                pyautogui.keyUp('ctrl')

                # time.sleep(0.1)  # Wait a bit for the copy command to execute
                text = pyperclip.paste()

                return text
            else:
                print("No active window detected.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        

    def init(self, context: ClickGPTContext):
        style = ttk.Style('superhero')
        self.tkroot = style.master
        self.tkroot.withdraw()
        
        keyboard.add_hotkey('ctrl+`', lambda: self.on_hotkey(context))

        self.tkroot.mainloop()

    def exit(self):
        print('Exiting ClickGPT')
        self.tkroot.destroy()
        sys.exit(0)
