import tkinter as tk
from tkinter import font, Frame, messagebox
from constants import *
from classes.userClass import User
from enum import Enum
class Application_Menu_State(Enum):
    SETUP_STEAM_URL = 0

class Application:
    def __init__(self):
        self.master_window = tk.Tk()
        self.__first_call_master_setup()
        self.__font_style_1 = font.Font(font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
        self.current_frame = None
        self.main_user = None

        self.__switch_menu_state(Application_Menu_State.SETUP_STEAM_URL)

        self.master_window.mainloop()

    '''user will provide their steam page url. this method calls the steamAPIScraper to get the users information.
    if main acount is private or url is invalid return None'''
    def __check_and_set_main_user(self, steam_page_url) -> User:
        pass

    def __first_call_master_setup(self):
        self.master_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.master_window.title(SCREEN_TITLE)
        self.master_window.resizable(False, False)
        self.master_window.configure(background=PRIMARY_COLOR)

    def __create_steam_url_frame(self):
        self.current_frame = tk.Frame()
        self.current_frame.configure(background=PRIMARY_COLOR)
        self.current_frame.pack(fill=tk.BOTH)
        welcome_text = tk.Label(self.current_frame, text="Please provide your Steam profile URL", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
        welcome_text.pack(pady=TITLE_TEXT_PADDING_Y)
        inputBox = tk.Text(self.current_frame, height=1, font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
        inputBox.pack(padx=int(SCREEN_WIDTH/6))
        button = tk.Button(self.current_frame, text="click me", font=('Arial', 18), bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR)
        button.pack()

    '''Takes a new state enum that represents what the application will be displaying. deletes frame then setup new frame'''
    def __switch_menu_state(self, new_state: Application_Menu_State):
        self.__clear_frame()
        match new_state:
            case Application_Menu_State.SETUP_STEAM_URL:
                self.__create_steam_url_frame()
            case _:
                pass
        pass

    '''Deletes all frame information'''
    def __clear_frame(self):
        if self.current_frame == None:
            return
        self.current_frame.destroy()