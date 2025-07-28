import os
import requests
import sys
import time
from userClass import User
from gameClass import Game
from utilityClass import Utility
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constants import STEAM_PROFILE_URL, WEBPAGE_WAIT_TIME, GAME_TAGS_LINK, ELUX_ID_TEMP

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

class MainUser(User):
    """
    Represents the primary user of the application, inheriting from the User class.
    This class adds a friend_list and custom behavior for generating its game list.
    """
    def __init__(self, user_id: str, name = "", game_list: list[Game] = None, is_account_private: bool = False, profile_image: str = None) -> None:
        super().__init__(user_id = user_id,
                         name = name,
                         game_list = game_list, # Needed for Tests
                         is_account_private = is_account_private,
                         profile_image = profile_image)
        if game_list is None:
            self.game_list = self.get_game_list()
        self.friend_list = self.get_friend_list()

    def get_friend_list(self) -> list[User]:
        """
        Returns a list of User objects, aka friends, with the following fields: 
        """

        friend_users = [] # each friend will be a user in the list

        if self.is_account_private == True:   # return error and instructions to set your profile to public
            raise Exception("profile is private")
        friends_list_link = STEAM_PROFILE_URL + self.user_id + "/friends/"

        response = requests.get(friends_list_link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')    #soup is the whole webpage

        for friend in soup.find_all("div", class_="friend_block_v2"):
           steam_id = friend.get("data-steamid")
           new_friend = Utility.create_user(steam_id)
           friend_users.append(new_friend)
        
        print(friend_users)
        return friend_users


        
    def get_game_list(self):
        if self.is_account_private == True:   # return error and instructions to set your profile to public
          raise Exception('profile is private')
        
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        game_list_url = GAME_TAGS_LINK + self.user_id

        driver.get(game_list_url)
        time.sleep(WEBPAGE_WAIT_TIME)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        games_table = soup.find('div', {'id' : 'Games'}) #the case matches now
        if games_table is None:
          raise Exception("error retrieving games list")    #site is down etc
        
        game_entries = games_table.find_all("li")
        for entry in game_entries:
          game_tag_list = []  #reset the list on each loop

          play_link = entry.find('a', class_='play-buy-link')     # get the app id from the 'play game' link
          app_id = play_link['href'].split('steam://run/')[-1] if play_link else None

          title_tag = entry.find('p', class_='title')    # grabbing the name of the game from the title field
          name = title_tag.get_text(strip=True) if title_tag else 'No Name Found'

          tags_table = entry.find('p', class_='tags')
          tag_spans = tags_table.find_all('span') if tags_table else []
          for tag in tag_spans:
            game_tag_list.append(tag.get_text(strip=True))

          hours_tag = entry.find('p', class_='hours')
          hours = 0.0   # default value so missing it doesn't crash    
          if hours_tag:
            hours_text = hours_tag.get_text(strip=True)
            if 'hrs' in hours_text:
              number_part = hours_text.split('hrs')[0].strip()
              try:
                hours = float(number_part)
              except ValueError:
                hours = 0.0

          header_img_tag = entry.find('div', class_='header').find('img')
          image_url = header_img_tag.get('src') if header_img_tag else None

          game = Game(app_id, name, game_tag_list, hours, image_url)
          self.game_list.append(game)

            
def main():
  player = MainUser(ELUX_ID_TEMP)
  #player.check_user_info()
  player.get_friend_list()
  
  
if __name__ == "__main__":
  main()