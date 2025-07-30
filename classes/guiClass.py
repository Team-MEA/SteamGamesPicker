import tkinter as tk
from tkinter import font, Frame, messagebox, ttk
from constants import *
from classes.userClass import User
from classes.gameClass import Game
from classes.utilityClass import Utility
from classes.sessionClass import Session
from classes.stateClass import State
from enum import Enum
import webbrowser
import os
import threading
import time
class Application_Menu_State(Enum):
    SETUP_STEAM_URL = 0
    DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION = 1
    CHOOSE_FRIENDS = 2
    FILTER_HOURS = 3
    FILTER_GENRE = 4
    SHARED_FRIENDS_GAME_LIST = 5
    PICKER_UI = 6
    PICKER_UI_CONTINUE = 7
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
        self.__session_class = None

        self.__switch_menu_state(Application_Menu_State.SETUP_STEAM_URL)

        self.master_window.mainloop()

    '''user will provide their steam page url. this method calls the steamAPIScraper to get the users information.
    if main acount is private or url is invalid return None'''
    # Changed to provide ID and program adds the URL
    def __check_and_set_main_user(self, steam_page_url) -> User:
        pass

    def __first_call_master_setup(self):
        self.master_window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.master_window.title(SCREEN_TITLE)
        self.master_window.resizable(False, False)
        self.master_window.configure(background=PRIMARY_COLOR)

    def __create_steam_url_frame(self):
        welcome_text = tk.Label(self.current_frame, text="Please provide your Steam ID", font=self.__font_header, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        welcome_text.pack(side=tk.TOP, pady=TITLE_TEXT_PADDING_Y)
        hyperlink = tk.Label(self.current_frame, text="quick link to steam profile settings", font=self.__font_style_2,bg=PRIMARY_COLOR ,fg=ACENT_COLOR, cursor="hand2")
        hyperlink.pack(pady=LABEL_PADDING_Y)
        hyperlink.bind("<Button-1>", lambda e: webbrowser.open_new(STEAM_PROFILE_URL))
        inputBox = tk.Entry(self.current_frame, width=int(SCREEN_WIDTH/14))
        inputBox.insert(0, STEAM_PLACEHOLDER_URL)
        inputBox.pack(pady=LABEL_PADDING_Y)
        button = tk.Button(self.current_frame, text="click me", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__button_steam_profile_call(inputBox.get(), button))
        button.pack()


    def __create_loading_screen(self, button):
        bar = ttk.Progressbar(self.current_frame, orient="horizontal", length=300, mode="determinate", maximum=100)
        bar.pack(pady=10)
        info_text = tk.Label(self.current_frame, text="Please wait while we identify your games and related tags...", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack(pady=LABEL_PADDING_Y)



        def update_progress():
            nonlocal progress_value
            if progress_value < 100:
                progress_value += int(100/WEBPAGE_WAIT_TIME)
                bar['value']+=int(100/WEBPAGE_WAIT_TIME)
                self.current_frame.after(1010, update_progress)  # Update every second
                self.current_frame.update_idletasks()
            else:
                self.current_frame.after(0, lambda: (
                    button.config(state='normal'),
                    bar.pack_forget(),
                    info_text.pack_forget()
                ))

        def do_fetch():
            self.main_user.game_list = self.main_user.get_game_list()
            #TODO XXX
            #REPLACE THE ABOVE "SELF.SLEEPS()" WITH STEAM SCRAPER API THAT CALLS THE MAIN USER AND SET IT TO SELF.MAIN_USER
            print("finished")
            self.__switch_menu_state(Application_Menu_State.DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION)
        bar.pack()
        button.config(state='disabled')
        progress_value = 0

        threading.Thread(target=do_fetch, daemon=True).start()
        update_progress()


    def __button_steam_profile_call(self, input_box, button_to_disable):
        user_input_text = input_box
        if user_input_text == "" or user_input_text == None or user_input_text == STEAM_PLACEHOLDER_URL:
            messagebox.showerror(self.current_frame, "URL is required")
            return
        #raise Exception("set up steamAPI interaction to retrieve main user")#TODO XXX
        #todo get the main users games, then friends
        steam_id = Utility.get_steamid_from_url(user_input_text)
        try:
            self.main_user = Utility.create_main_user(steam_id)
        except Exception as e:
            messagebox.showerror(self.current_frame, f"Private account or invalid...\n{e}")
            self.__switch_menu_state(Application_Menu_State.SETUP_STEAM_URL)
            return
        print("valid account")
        self.__create_loading_screen(button_to_disable)

    
    def __button_find_common_friends_games(self):
        self.__switch_menu_state(Application_Menu_State.CHOOSE_FRIENDS)
    
    def __button_get_hour_selection(self):
        self.__switch_menu_state(Application_Menu_State.FILTER_HOURS)

    def __button_pick_random_game(self, game_list):
        self.final_game_result = Utility.get_random_selection(game_list)
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
        left_game_display_frame.pack(side="right", fill="both", padx=(GAME_LIST_FRAM_PADDING, 0))
        scroll_bar = ttk.Scrollbar(self.current_frame, orient="vertical", command=left_game_display_frame.yview)
        scroll_bar.pack(side="right", fill=tk.Y)
        left_game_display_frame.config(scrollregion=left_game_display_frame.bbox("all"))
        

        try:
            for i in range(len(game_list)):
                container_for_game_objects = tk.Frame(left_game_display_frame, bg=ACENT_COLOR)
                left_game_display_frame.create_window(DISTANCE_FROM_WEST_WALL, i * GAME_OBJECT_PADDING_Y, window=container_for_game_objects, height=30, width= int(SCREEN_WIDTH), anchor="center")
                game_name = tk.Label(container_for_game_objects, text=f"{game_list[i]}", font=self.__font_style_1, background=ACENT_COLOR)
                game_name.pack(padx=25, anchor="center", fill="both")
        except Exception as e:
            print(f"main_user not yet implemented can load list {e}")

        return right_display, left_game_display_frame

    def __create_game_list_frame(self):
        #TODO XXX
        print("TODO: GET NEEDED INFORMAION FROM MAIN_USER")
        #where the function below calls a bunch of game objects, replace it with self.main_user.game_list
        right_display, left_game_display_frame = self.__create_left_andr_right_frames(self.main_user.game_list)#[Game(12345, "Counter-Strike 2", None, 0), Game(45678, "Dark Souls", None, 0), Game(621, "Peak", None, 0), Game(622111, "Ready or Not", None, 0), Game(646542, "FINAL FANTASY XIV Online", None, 0), Game(64642542, "Apex Legends", None, 0), Game(1111, "DeltaRune", None, 0), Game(646542, "Deus Ex", None, 0)])
        find_common_games_friends = tk.Button(right_display, text="Find common games\nwith your friends", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=THIRDARY_COLOR,command=self.__button_find_common_friends_games)
        find_common_games_friends.pack( pady=60)
        pick_random_game = tk.Button(right_display, text="Pick random game from library", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=THIRDARY_COLOR, command=self.__button_get_hour_selection)
        pick_random_game.pack()
        #TODO XXX
        #help_pick. replace command with command=lambda: self.__button_filter_out_genres(self.main_user.game_list)
        help_pick = tk.Button(right_display, text="Help me pick a game", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=THIRDARY_COLOR, command=lambda: self.__button_filter_out_genres(self.main_user.game_list ))#[Game(12345, "Counter-Strike", ["fps", "russian", "stimky"], 0), Game(45678, "Minecraft", ["fps", "building", "sim", "AVERYLONGTAGNAMEFORSOMEREASON"], 0), Game(621, "hog warts", ["hog wartz"], 0), Game(698695621, "hog w10arts", ["hog wartz"], 0), Game(621968986, "hog9 warts", ["hog wartz"], 0), Game(62532161, "hog 8warts", ["hog wartz"], 0), Game(412341621, "hog 7warts", ["hog wartz"], 0), Game(62643221, "hog 6warts", ["hog wartz"], 0), Game(62753471, "hog 5warts", ["hog wartz"], 0), Game(6275246421, "hog 4warts", ["hog wartz"], 0), Game(6643643221, "hog w3arts", ["hog wartz"], 0), Game(6232321, "hog 2warts", ["hog wartz"], 0), Game(623321, "hog 1warts", ["hog wartz"], 0)]))
        help_pick.pack(pady=60)

    def __picker_undo(self):
        self.__session_class.undo()
        self.__switch_menu_state(Application_Menu_State.PICKER_UI_CONTINUE)
    def __picker_redo(self):
        self.__session_class.redo()
        self.__switch_menu_state(Application_Menu_State.PICKER_UI_CONTINUE)
    def __picker_reset(self):
        self.__session_class.reset()
        self.__switch_menu_state(Application_Menu_State.PICKER_UI)

    def __picker_next(self, checkboxs):
        for x in checkboxs:
            if checkboxs[x].get() == True:
                for y in self.__session_class.history_array[self.__session_class.current_index].batch:
                    if x == y:
                        print(y)
                        y.switch_selection()
        self.__session_class.confirm()
        print(f"final pick is {self.__session_class.history_array[self.__session_class.current_index].final_pick}")
        if self.__session_class.history_array[self.__session_class.current_index].final_pick != None:
            print("am i printing")
            self.final_game_result = self.__session_class.history_array[self.__session_class.current_index].final_pick
            self.__switch_menu_state(Application_Menu_State.END_STATE)
            return
        else:
            self.__switch_menu_state(Application_Menu_State.PICKER_UI_CONTINUE)
        
        

        


    def __create_picker_frame(self):
        info_text = tk.Label(self.current_frame, text="Let us help you narrow down your choice!\nSelect the games you or your friends prefer to play", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack(pady=LABEL_PADDING_Y)
        
        right_display = tk.Frame(self.current_frame,  borderwidth=BORDER_WIDTH, background=PRIMARY_COLOR, relief="groove")
        right_display.pack(side="right", fill="both")
        redo_button = tk.Button(right_display, text="REDO", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=self.__picker_redo)
        redo_button.pack()
        undo_button = tk.Button(right_display, text="UNDO", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=self.__picker_undo)
        undo_button.pack()
        reset_button = tk.Button(right_display, text="RESET", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=self.__picker_reset)
        reset_button.pack()

        left_display = tk.Canvas(self.current_frame, borderwidth=BORDER_WIDTH, background=PRIMARY_COLOR, relief="groove")
        left_display.pack(side="right", fill="both", expand=True)
        next_button = tk.Button(right_display, text="next", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__picker_next(checkboxs))
        next_button.pack(side="bottom")

        
        current_colm_count = 0
        current_row_count = 0
        checkboxs = {}
        self.__session_class.history_array[self.__session_class.current_index].batch
        for x in range(len(self.__session_class.history_array[self.__session_class.current_index].batch)):
            
            if current_colm_count == GRID_MAX_COLUMS:
                current_colm_count = 0
                current_row_count += 1
            boolean_check = tk.BooleanVar()
            checkboxs[self.__session_class.history_array[self.__session_class.current_index].batch[x]] = boolean_check
            selection_bool = tk.Checkbutton(left_display, text=self.__text_cutoff(self.__session_class.history_array[self.__session_class.current_index].batch[x].name), variable=boolean_check, font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, selectcolor="black")
            selection_bool.grid(row=current_row_count, column=current_colm_count, sticky='news', pady=0)
            current_colm_count += 1
        

        
    def __create_frame_to_filter_hours(self):
        #TODO XXX
        print("TODO: GET NEEDED INFORMAION FROM MAIN_USER")
        #where the function below calls a bunch of game objects, replace it with self.main_user.game_list
        PLACE_HOLDER_LIST = [Game(12345, "Counter-Strike", None, 100), Game(45678, "Minecraft", None, 10), Game(621, "hog warts", None, 0)]
        right_display, left_game_display_frame = self.__create_left_andr_right_frames(self.main_user.game_list)
        info_text = tk.Label(right_display, text="Randomly pick a game\nbased off total hours played", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack()
        slider = tk.Scale(right_display, from_=0, to=150, orient=tk.HORIZONTAL, length=int(SCREEN_WIDTH/4))
        slider.pack()
        hours_button = tk.Button(right_display, text="Pick a random game\nwithin selected hours", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR,command=lambda:  self.__button_pick_random_game(Utility.reduce_games_list_from_hours(slider.get(), self.main_user.game_list)))
        hours_button.pack(pady=20)
        random_button = tk.Button(right_display, text="Pick at random!", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR,fg=ACENT_COLOR, command=lambda:  self.__button_pick_random_game(self.main_user.game_list))
        random_button.pack(pady=20)

    def __create_genre_selection_filtering(self):
        info_text = tk.Label(self.current_frame, text="Select the genres you want to filter for\nDon't select any to skip", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack(pady=LABEL_PADDING_Y)
        checkboxs = {}
        current_colm_count = 0
        current_row_count = 0
        frame_buttons, frame_canvas, canvas, vsb = self.__create_grid_selection()

        genres_tags = Utility.get_all_tags_from_games_list(self.filtered_game_list)

        for x in range(len(genres_tags)):
            if current_colm_count == 5:
                current_colm_count = 0
                current_row_count += 1
            boolean_check = tk.BooleanVar()
            checkboxs[genres_tags[x]] = boolean_check
            selection_bool = tk.Checkbutton(frame_buttons, text=self.__text_cutoff(genres_tags[x]), variable=boolean_check, font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR,selectcolor="black")
            selection_bool.grid(row=current_row_count, column=current_colm_count, sticky='news', pady=0)
            current_colm_count += 1

        frame_buttons.update_idletasks()
        frame_canvas.config(width=500 + vsb.winfo_width(),height=0)
        canvas.config(scrollregion=canvas.bbox("all"))

        continue_button = tk.Button(self.current_frame, text="continue", bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__sift_through_genres(checkboxs))
        continue_button.pack()

    def __sift_through_genres(self, checkboxs):
        selected_genres = []
        for x in checkboxs:
            if checkboxs[x].get() == True:
                selected_genres.append(x)
        new_filtered_game_list = Utility.reduce_games_list_from_tags(selected_genres, self.filtered_game_list)
        if len(new_filtered_game_list) == 0:
            messagebox.showerror(self.current_frame, "No games exist with selected tag(s)")
        else:
            self.filtered_game_list = new_filtered_game_list
            self.__switch_menu_state(Application_Menu_State.PICKER_UI)


    def __create_grid_selection(self) ->tuple[tk.Frame, tk.Canvas, tk.Canvas, tk.Scrollbar]:
        grid_frame = tk.Frame(self.current_frame)
        grid_frame.pack()
        
        frame_main = tk.Frame(grid_frame, bg=PRIMARY_COLOR)
        frame_main.grid(sticky='news')
        
        frame_canvas = tk.Frame(frame_main)
        frame_canvas.grid(row=2, column=0, pady=(CHECKLIST_TOP_Y_PATTING, CHECKLIST_BOTTOM_Y_PATTING), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_propagate(True)
        canvas = tk.Canvas(frame_canvas, bg=SECONDARY_COLOR, width=700)
        canvas.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        frame_buttons = tk.Frame(canvas, bg=SECONDARY_COLOR)
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        return (frame_buttons,frame_canvas,canvas, vsb) 

    def __create_friends_selection(self):
        info_text = tk.Label(self.current_frame, text="Select friends you want to find common games between", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack(pady=LABEL_PADDING_Y)
        checkboxs = {}
        current_colm_count = 0
        current_row_count = 0

        frame_buttons, frame_canvas, canvas, vsb = self.__create_grid_selection()
        
        #TODO XXX
        print("TODO, CHECKLIST WONT FUNCTION UNTIL FRIENDS LIST IS IMPLEMENTED. ADDING FAKE VALUES...")
        #for loop should go based off len of friends list and instead of m, display user name. checkboxs[x] instead of x, it should store the name of the friend
        for x in range(len(self.main_user.friend_list)):
            temp_name = self.main_user.friend_list[x].username
            if current_colm_count == GRID_MAX_COLUMS:
                current_colm_count = 0
                current_row_count += 1
            boolean_check = tk.BooleanVar()
            checkboxs[temp_name] = boolean_check
            selection_bool = tk.Checkbutton(frame_buttons, text=self.__text_cutoff(temp_name), variable=boolean_check, font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR,selectcolor="black")
            selection_bool.grid(row=current_row_count, column=current_colm_count, sticky='news', pady=0)
            current_colm_count += 1

        frame_buttons.update_idletasks()
        frame_canvas.config(width=500 + vsb.winfo_width(),height=0)
        canvas.config(scrollregion=canvas.bbox("all"))

        continue_button = tk.Button(self.current_frame, text="continue", bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__sift_through_users_friends_selection(checkboxs))
        continue_button.pack()

    def __text_cutoff(self,text):
        if len(text) > CHECKLIST_MAX_CHAR_LENGTH:
            return (text[:CHECKLIST_MAX_CHAR_LENGTH - 3] + "...")
        return text
    
    def __friends_filtered_list(self):

        right_display, left_game_display_frame = self.__create_left_andr_right_frames(self.filtered_game_list)
        pick_random_game = tk.Button(right_display, text="Pick random game\nfrom shared library", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=THIRDARY_COLOR, command=lambda: self.__button_pick_random_game(self.filtered_game_list))
        pick_random_game.pack()
        help_pick = tk.Button(right_display, text="Help me pick a game", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=THIRDARY_COLOR, command=lambda: self.__button_filter_out_genres(self.filtered_game_list ))
        help_pick.pack(pady=60)


    def __sift_through_users_friends_selection(self, checkboxs):
        ##TODO XXX
        #THIS FUCNTION WILL NOT WORK UNTIL USERCLASS IS IMPLEMENTED
        print("this function will not work until userclass is implmeneted")
        selected_friends_list = []
        for x in checkboxs:
            if checkboxs[x].get() == True:
                selected_friends_list.append(x)
        #not great, but im running out of time to midmax this
        true_selected_friends_list = []
        for x in self.main_user.friend_list:
            if x.username in selected_friends_list:
                print(f"{x.username} was selected")
                x.get_games_list_quick()
                user_id, username, is_account_private, signature= Utility.get_user_info(x.user_id)
                x.is_account_private = is_account_private
                true_selected_friends_list.append(x)
                
        #TODO
        #generate friends games then look for common games
        print(true_selected_friends_list[0].game_list)
        self.filtered_game_list = Utility.find_common_games(self.main_user, true_selected_friends_list)
        #print(self.filtered_game_list)
        self.__switch_menu_state(Application_Menu_State.SHARED_FRIENDS_GAME_LIST)

    def __create_end_screen(self):
        start_text = tk.Label(self.current_frame, text=f"Your choosen result is...", font=self.__font_style_1, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        start_text.pack()
        info_text = tk.Label(self.current_frame, text=f"{self.final_game_result}", font=self.__font_header, bg=PRIMARY_COLOR, fg=THIRDARY_COLOR)
        info_text.pack(pady=FINAL_GAME_RESULT_PADDING_Y)
        #TODO
        #i cannot confirm if start_game_button works or not
        start_game_button = tk.Button(self.current_frame, text="run game", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: os.system(f"{STEAM_RUN_COMMAND}{self.final_game_result.app_id}"))
        start_game_button.pack(pady=20)
        back_to_main = tk.Button(self.current_frame, text=" go back to main", font=self.__font_style_1, bg=SECONDARY_COLOR, highlightbackground=ACENT_COLOR, fg=ACENT_COLOR, command=lambda: self.__switch_menu_state(Application_Menu_State.DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION))
        back_to_main.pack(pady=20)


    '''Takes a new state enum that represents what the application will be displaying. deletes frame then setup new frame'''
    def __switch_menu_state(self, new_state: Application_Menu_State):
        self.__clear_frame()
        match new_state:
            case Application_Menu_State.SETUP_STEAM_URL:
                self.__init_frame()
                self.__create_steam_url_frame()
            case Application_Menu_State.DISPLAY_GAME_LIST_WITH_FRIENDS_OPTION:
                self.__session_class = None
                self.__list_seen_games = []
                self.__init_frame()
                self.__create_game_list_frame()
            case Application_Menu_State.CHOOSE_FRIENDS:
                self.__init_frame()
                self.__create_friends_selection()
            case Application_Menu_State.FILTER_HOURS:
                self.__init_frame()
                self.__create_frame_to_filter_hours()
            case Application_Menu_State.FILTER_GENRE:
                self.__init_frame()
                self.__create_genre_selection_filtering()
            case Application_Menu_State.PICKER_UI:
                self.__init_frame()
                self.__session_class = Session(self.filtered_game_list)
                self.__create_picker_frame()
            case Application_Menu_State.PICKER_UI_CONTINUE:
                self.__init_frame()
                self.__create_picker_frame()
            case Application_Menu_State.SHARED_FRIENDS_GAME_LIST:
                self.__init_frame()
                self.__friends_filtered_list()
            case Application_Menu_State.END_STATE:
                self.__init_frame()
                self.__create_end_screen()
            case _:
                pass
        pass

    '''Deletes all frame information'''
    def __clear_frame(self):
        if self.current_frame == None:
            return
        self.current_frame.destroy()
