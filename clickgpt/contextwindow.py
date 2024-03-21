from __future__ import annotations
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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


class ContextWindow(ttk.Toplevel):
    req_field: ttk.Text
    res_field: ttk.Text
    copypaste_button: ttk.Button
    was_created: bool

    def __init__(self) -> None:
        ttk.Toplevel.__init__(self)
        
        self.was_created = False
        self.title("ClickGPT")
        pass

    def create(self, options:dict[str, TextOption], option_select_callback):
        
        self.attributes('-topmost',True)  #for focus on toplevel

        self.req_field = ttk.Text(self, width=70, height=4, wrap=ttk.WORD)
        self.req_field.grid(row=0, column=0)

        self.res_field = ttk.Text(self, width=70, height=4, wrap=ttk.WORD)
        self.res_field.grid(row=1, column=0)

        self.copypaste_button = ttk.Button(self, text="Copy Paste", bootstyle=SUCCESS, command=lambda: self.copy_paste_close())
        self.copypaste_button.grid(row=1, column=1)

        options_label_string = ttk.StringVar()
        options_label_string.set("Select action")

        options_label = ttk.OptionMenu(self, options_label_string, ())
        options_label.grid(row=0, column=1)

        menu = options_label["menu"]
        menu.delete(0, 1) # remove first element because it gets created and we want to fill everything dynamically

        self.fill_options_recursive(menu, options, option_select_callback)

        # get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        x = ws/2
        y = hs/2

        # set where it is placed
        self.geometry('+%d+%d'%(x, y))

        print('Show context window')
        

    def fill_options_recursive(self, menu: ttk.Menu | ttk.OptionMenu, options: dict[str, TextOption], option_select_callback):
        for (key, option) in options.items():
            if option.options:
                sublist = ttk.Menu(menu, tearoff=False)
                menu.add_cascade(label=option.name, menu=sublist)

                self.fill_options_recursive(sublist, option.options, option_select_callback)
            else:
               callback = lambda key=key, option=option: option_select_callback(key, option)
               menu.add_command(label=option.name, command=callback)

    def set_request_text(self, text:str):
        self.req_field.insert(ttk.END, text)

    def set_response_text(self, text:str):
        self.res_field.insert(ttk.END, text)

    def get_request_text(self) -> str:
        return self.req_field.get("1.0",ttk.END)

    def get_response_text(self) -> str:
        return self.res_field.get("1.0",ttk.END)

    def copy_paste_close(self):
        response = self.get_response_text().rstrip()
        print(response)
        pyperclip.copy(response)

        print('Hiding context window')

        self.destroy()

        print('Pasting response')

        time.sleep(0.3)
        pyautogui.keyDown('ctrl')
        time.sleep(0.01)
        pyautogui.keyDown('v')
        time.sleep(0.01)
        pyautogui.keyUp('v')
        time.sleep(0.01)
        pyautogui.keyUp('ctrl')
    