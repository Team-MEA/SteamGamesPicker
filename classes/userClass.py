import os
import sys
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


child_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(child_dir, '..'))     # unsure if necesary, seems to only be needed on my setup for some reason, try commenting out and see if it works if anyone uses this
sys.path.append(parent_dir)


from constants import STEAM_ID_LINK, GAME_TAGS_LINK, WEBPAGE_WAIT_TIME, STEAM_ID_URL, ELUX_ID_TEMP
from gameClass import Game

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




class User:

  def __init__(self, user_id: str, name = "", game_list: list[Game] = None, is_account_private: bool = True, profile_image: str = None) -> None:
    self.user_id = user_id
    self.username = name
    if game_list is None:
            self.game_list = self.get_games_list_quick()
    else:
       self.game_list = game_list # Needed for Tests
    self.is_account_private = is_account_private
    self.profile_image = profile_image

  def __str__(self):
        """
        Returns a user-friendly string representation of the User object, which is its name.
        """
        return self.username
  
  def __repr__(self):
        """
        Returns an unambiguous string representation of the User object. By default, it uses the __str__ method.
        """
        return self.__str__()

  def check_user_info(self): # check to see the privacy status of the user profile    MOVED TO UTILITY CLASS, CAN BE DELETED FROM HERE
    user_id_link = STEAM_ID_LINK + self.user_id

    response = requests.get(user_id_link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')    #soup is the whole webpage
      
    info_table = soup.find("table", id = "profile-info")
    if info_table is None:
      raise Exception("lookup failed, invalid ID")
    search_string = "profile state"

    table_rows = info_table.find_all("tr")
    for child in table_rows:
      if search_string in child.get_text(strip=True).lower():
        if "public" in child.get_text(strip=True).lower():
          self.is_account_private = False   # if both are correct, the profile is private
          break
        else:                               # there is only 2 states, so if it's not public raise an error (friends only also reads as private, and unreachable)
          raise Exception("profile is private")
    else:    
      raise Exception("lookup failed")
    
    if self.is_account_private == False:    #Only continue if the profile is set to public
      for row in table_rows:
        row_text = row.get_text(strip=True).lower()
        if row_text.startswith("name"):
          self.username = row_text.split("name")[1].strip()
          break
      else:
        raise Exception("username not found")
    
    

  def get_games_list_quick(self):
    games_link = STEAM_ID_URL + self.user_id + "/games?xml=1"

    response = requests.get(games_link)
    soup = BeautifulSoup(response.content, "xml")

    games = soup.find_all("game")

    game_data = [ # create the list immediately so that you only need to loop once
       (
          game.find("appID").text.strip(),
          game.find("name").text.strip()
       )
       for game in games    # want to try and see if I can move this before the list to make it easier to read
    
    return game_data




                #For testing, leave commented
'''def main():
  player = User(ELUX_ID_TEMP)
  #player.check_user_info()
  player.get_games_list_quick()
  
  
if __name__ == "__main__":
  main()'''