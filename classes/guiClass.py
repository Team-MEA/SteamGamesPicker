import tkinter as tk
from tkinter import font, Frame
from constants import *

class GUI:
    def __init__(self):
        self.master_window = tk.Tk()
        self.__first_call_master_setup()
        self.__font_style_1 = font(DEFAULT_FONT, DEFAULT_FONT_SIZE)


    def __first_call_master_setup(self):
        self.master_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.master_window.title(SCREEN_TITLE)
        self.master_window.resizable(False, False)
        self.master_window.configure(background=PRIMARY_COLOR)