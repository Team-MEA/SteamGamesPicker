import tkinter as tk
from tkinter import font, Frame, messagebox, ttk
from constants import *
from classes.userClass import User
from classes.gameClass import Game
from enum import Enum
import webbrowser
class Application_Menu_State(Enum):
    SETUP_STEAM_URL = 0
    DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION = 1
    CHOOSE_FRIENDS = 2
    FILTER_HOURS = 3
    FILTER_GENRE = 4
    END_STATE = 99

class Application:
    def __init__(self):
        self.master_window = tk.Tk()
        self.__first_call_master_setup()
        self.__font_style_1 = font.Font(font=(DEFAULT_FONT, DEFAULT_FONT_SIZE))
        self.__font_header = font.Font(font=(DEFAULT_FONT, HEADER_FONT_SIZE))
        self.__font_style_2 = font.Font(font=(DEFAULT_FONT, SMALL_FONT_SIZE))
        self.current_frame = None
        self.main_user = None
        self.filtered_game_list = None
        self.final_game_result = None

        self.__switch_menu_state(Application_Menu_State.DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION)

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
        welcome_text = tk.Label(self.current_frame, text="Please provide your Steam profile URL", font=self.__font_header, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        welcome_text.pack(side=tk.TOP, pady=TITLE_TEXT_PADDING_Y)
        hyperlink = tk.Label(self.current_frame, text="quick link to steam profile", font=self.__font_style_2,bg=PRIMARY_COLOR ,fg=ACENT_COLOR, cursor="hand2")
        hyperlink.pack(pady=LABEL_PADDING_Y)
        hyperlink.bind("<Button-1>", lambda e: webbrowser.open_new(STEAM_PROFILE_URL))
        inputBox = tk.Entry(self.current_frame, width=int(SCREEN_WIDTH/14))
        inputBox.insert(0, STEAM_PLACEHOLDER_URL)
        inputBox.pack(pady=LABEL_PADDING_Y)
        button = tk.Button(self.current_frame, text="click me", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__button_steam_profile_call(inputBox))
        button.pack()

    def __button_steam_profile_call(self, input_box):
        user_input_text = input_box.get()
        if user_input_text == "" or user_input_text == None or user_input_text == STEAM_PLACEHOLDER_URL:
            messagebox.showerror(self.current_frame, "URL is required")
            return
        raise Exception("set up steamAPI interaction to retrieve main user")#TODO
        #todo call steam api, provide the userinput url and get a mainuser object from steam api.
        #store mainuser object in self.main_user. if error, or invalid user, showerror
    
    def __button_find_common_friends_games(self):
        self.__switch_menu_state(Application_Menu_State.CHOOSE_FRIENDS)
    
    def __button_get_hour_selection(self):
        self.__switch_menu_state(Application_Menu_State.FILTER_HOURS)

    def __button_pick_random_game(self, game_list):
        #TODO
        print("TODO add funcitonality")
        #call the utilityclass with provided game_list and get choosen game. set it to self.final_game_result
        self.__switch_menu_state(Application_Menu_State.END_STATE)

    def __button_filter_out_genres(self, game_list):
        self.filtered_game_list = game_list
        self.__switch_menu_state(Application_Menu_State.FILTER_GENRE)

    def __init_frame(self):
        self.current_frame = tk.Frame(self.master_window)
        self.current_frame.configure(background=PRIMARY_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def __create_left_andr_right_frames(self, game_list) -> tuple[tk.Frame, tk.Canvas]:
        right_display = tk.Frame(self.current_frame,  borderwidth=BORDER_WIDTH, background=PRIMARY_COLOR, relief="groove")
        right_display.pack(side="right", expand=True, fill="both")
        left_game_display_frame = tk.Canvas(self.current_frame, borderwidth=BORDER_WIDTH, background=PRIMARY_COLOR, relief="groove")
        left_game_display_frame.pack(side="right", fill="both")
        scroll_bar = ttk.Scrollbar(self.current_frame, orient="vertical", command=left_game_display_frame.yview)
        scroll_bar.pack(side="right", fill=tk.Y)
        left_game_display_frame.config(yscrollcommand=scroll_bar.set)

        try:
            for i in range(len(game_list)):
                container_for_game_objects = tk.Frame(left_game_display_frame, bg=ACENT_COLOR)
                left_game_display_frame.create_window(DISTANCE_FROM_WEST_WALL, i * GAME_OBJECT_PADDING_Y, window=container_for_game_objects, height=30, width= int(SCREEN_WIDTH))
                game_name = tk.Label(container_for_game_objects, text=f"{game_list[i]}")
                game_name.pack()
        except Exception as e:
            print(f"main_user not yet implemented can load list {e}")

        return right_display, left_game_display_frame

    def __create_game_list_frame(self):
        #TODO
        print("TODO: GET NEEDED INFORMAION FROM MAIN_USER")
        #where the function below calls a bunch of game objects, replace it with self.main_user.game_list
        right_display, left_game_display_frame = self.__create_left_andr_right_frames([Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)])
        
        find_common_games_friends = tk.Button(right_display, text="Find common games\nwith your friends", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, command=self.__button_find_common_friends_games)
        find_common_games_friends.pack( pady=20)
        pick_random_game = tk.Button(right_display, text="Pick random game from library", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, command=self.__button_get_hour_selection)
        pick_random_game.pack()
        help_pick = tk.Button(right_display, text="Help me pick a game", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, command=lambda: self.__button_filter_out_genres(self.main_user.game_list))
        help_pick.pack(pady=20)

        
    def __create_frame_to_filter_hours(self):
        #TODO
        print("TODO: GET NEEDED INFORMAION FROM MAIN_USER")
        #where the function below calls a bunch of game objects, replace it with self.main_user.game_list
        right_display, left_game_display_frame = self.__create_left_andr_right_frames([Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)])
        info_text = tk.Label(right_display, text="Randomly pick a game\nbased off total hours played", font=self.__font_style_1)
        info_text.pack()
        slider = tk.Scale(right_display, from_=0, to=150, orient=tk.HORIZONTAL, length=int(SCREEN_WIDTH/4))
        slider.pack()
        help_pick = tk.Button(right_display, text="Help me pick a game", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, command=lambda: print(slider.get()))
        help_pick.pack(pady=20)

    '''Takes a new state enum that represents what the application will be displaying. deletes frame then setup new frame'''
    def __switch_menu_state(self, new_state: Application_Menu_State):
        self.__clear_frame()
        match new_state:
            case Application_Menu_State.SETUP_STEAM_URL:
                self.__init_frame()
                self.__create_steam_url_frame()
            case Application_Menu_State.DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION:
                self.__init_frame()
                self.__create_game_list_frame()
            case Application_Menu_State.CHOOSE_FRIENDS:
                #TODO
                print("choose friend ui function needs to be implemented")
            case Application_Menu_State.FILTER_HOURS:
                self.__init_frame()
                self.__create_frame_to_filter_hours()
            case Application_Menu_State.FILTER_GENRE:
                #TODO
                print("call util for genre list and let user select filters")
            case _:
                pass
        pass

    '''Deletes all frame information'''
    def __clear_frame(self):
        if self.current_frame == None:
            return
        self.current_frame.destroy()