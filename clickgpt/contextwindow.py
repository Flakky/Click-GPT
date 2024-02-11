import tkinter as tk
import pyperclip
import pyautogui
import time
from typing import List

class TextOption:
    tag:str
    name:str

    def __init__(self, tag:str, name:str) -> None:
        self.tag = tag
        self.name = name

class ContextWindow:
    window: tk.Tk
    req_field: tk.Text
    res_field: tk.Text
    copypaste_button: tk.Button


    def __init__(self) -> None:
        pass

    def create(self, options:List[TextOption], option_select_callback) -> tk.Tk:
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

        sublist = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Text", menu=sublist)

        for option in options:
            sublist.add_command(label=option.name, command=lambda:option_select_callback(option.tag))

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
        pyperclip.copy(self.res_field.get("1.0",tk.END))
        self.window.destroy()
        time.sleep(0.3)
        pyautogui.keyDown('ctrl')
        time.sleep(0.01)
        pyautogui.keyDown('v')
        time.sleep(0.01)
        pyautogui.keyUp('v')
        time.sleep(0.01)
        pyautogui.keyUp('ctrl')
    