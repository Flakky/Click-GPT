from __future__ import annotations
import tkinter as tk
import pyperclip
import pyautogui
import time
from typing import List


class TextOption:
    name:str
    request:str
    options:dict[str, TextOption] | None
    
    def __init__(self) -> None:
        self.name = ""
        self.request = ""
        self.options = {}


    @classmethod
    def from_dict(cls, data:dict) -> TextOption:
        option = cls()
        option.name = data['name']
        option.request = data.get('request')
        options = data.get('options')
        if options is not None:
            for (key, val) in options.items():
                option.options[key] = cls.from_dict(val)

        return option


class ContextWindow:
    window: tk.Tk
    req_field: tk.Text
    res_field: tk.Text
    copypaste_button: tk.Button


    def __init__(self) -> None:
        pass

    def create(self, options:dict[str, TextOption], option_select_callback) -> tk.Tk:
        self.window = tk.Tk()
        self.window.title("ClickGPT")
        self.window.attributes('-topmost',True)  #for focus on toplevel

        self.req_field = tk.Text(self.window, width=70, height=4, wrap=tk.WORD)
        self.req_field.grid(row=0, column=0)

        self.res_field = tk.Text(self.window, width=70, height=4, wrap=tk.WORD)
        self.res_field.grid(row=1, column=0)

        self.copypaste_button = tk.Button(self.window, text="Copy Paste", padx=10, command=lambda: self.copy_paste_close())
        self.copypaste_button.grid(row=1, column=1)

        options_label_string = tk.StringVar()
        options_label_string.set("Select action")

        options_label = tk.OptionMenu(self.window, options_label_string, ())
        options_label.grid(row=0, column=1)

        menu = options_label["menu"]
        menu.delete(0, 1) # remove first element because it gets created and we want to fill everything dynamically

        self.fill_options_recursive(menu, options, option_select_callback)

    def fill_options_recursive(self, menu: tk.Menu | tk.OptionMenu, options: dict[str, TextOption], option_select_callback):
        for (key, option) in options.items():
            if option.options:
                sublist = tk.Menu(menu, tearoff=False)
                menu.add_cascade(label=option.name, menu=sublist)

                self.fill_options_recursive(sublist, option.options, option_select_callback)
            else:
               callback = lambda key=key, option=option: option_select_callback(key, option)
               menu.add_command(label=option.name, command=callback)

    def show(self):
        # get screen width and height
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()

        x = ws/2
        y = hs/2

        # set where it is placed
        self.window.geometry('+%d+%d'%(x, y))
        self.window.mainloop()

    def set_request_text(self, text:str):
        self.req_field.insert(tk.END, text)

    def set_response_text(self, text:str):
        self.res_field.insert(tk.END, text)

    def get_request_text(self) -> str:
        return self.req_field.get("1.0",tk.END)

    def get_response_text(self) -> str:
        return self.res_field.get("1.0",tk.END)

    def copy_paste_close(self):
        response = self.get_response_text().rstrip()
        print(response)
        pyperclip.copy(response)
        self.window.destroy()
        time.sleep(0.3)
        pyautogui.keyDown('ctrl')
        time.sleep(0.01)
        pyautogui.keyDown('v')
        time.sleep(0.01)
        pyautogui.keyUp('v')
        time.sleep(0.01)
        pyautogui.keyUp('ctrl')
    