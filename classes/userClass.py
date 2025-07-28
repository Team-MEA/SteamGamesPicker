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
from classes.gameClass import Game

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




class User:

  def __init__(self, user_id: str, name: str, game_list: list[Game] = None, is_account_private: bool = True, profile_image: str = None) -> None:
    self.user_id = user_id
    self.username = name
    self.game_list = game_list
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


  def get_games_list_quick(self):
    games_link = STEAM_ID_URL + self.user_id + "/games?xml=1"

    response = requests.get(games_link)
    soup = BeautifulSoup(response.content, "xml")

    games = soup.find_all("game")

    new_game_list = []

    for game in games:
        new_game_list.append(Game(game.find("appID").text.strip(), game.find("name").text.strip()))

    self.game_list = new_game_list

                #For testing, leave commented
'''def main():
  player = User(ELUX_ID_TEMP)
  #player.check_user_info()
  player.get_games_list_quick()
  
  
if __name__ == "__main__":
  main()'''