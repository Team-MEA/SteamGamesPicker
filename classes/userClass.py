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

from constants import STEAM_ID_LINK, GAME_TAGS_LINK, WEBPAGE_WAIT_TIME
from gameClass import Game

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




class User:

  def __init__(self, user_id: str, name: str, game_list: list[Game] = None, is_account_private: bool = True, profile_image: str = None) -> None:
    self.user_id = user_id
    self.username = name
    if game_list is None:
            self.game_list = self.get_game_list()
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

  def get_game_list(self):
    if self.is_account_private == True:   # return error and instructions to set your profile to public
      raise Exception('profile is private')
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options) # this and 2 lines above it are meant to keep the webpage from popping up, doesn't seem to be working though

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



                #For testing, leave commented
#def main():
  #player = User("76561198032787571")
  #player.check_user_info()
  #print(player.username)
  
  
#if __name__ == "__main__":
  #main()