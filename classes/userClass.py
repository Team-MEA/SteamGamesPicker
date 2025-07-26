import os
import sys
import requests

child_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(child_dir, '..'))     # unsure if necesary, seems to only be needed on my setup for some reason, try commenting out and see if it works if anyone uses this
sys.path.append(parent_dir)
from constants import STEAM_ID_LINK, GAME_TAGS_LINK
from bs4 import BeautifulSoup
import os

headers = {         # scraper does not work without this, this was the auto-complete but it seems to work
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




class User:
  def __init__(self, user_id, friend_list = [], game_list = [], is_account_private = True, profile_image = None):
    self.user_id = user_id
    self.friend_list = friend_list
    self.game_list = game_list
    self.is_account_private = is_account_private
    self.profile_image = profile_image

  def __str__(self):
        return self.user_id

  def check_privacy_setting(self): # check to see the privacy status of the user profile
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
    

  

  def get_game_list(self):
    if self.is_account_private == True:   # return error and instructions to set your profile to public
      raise Exception("profile is private")

  def get_friend_list(self):
    if self.is_account_private == True:   # return error and instructions to set your profile to public
      raise Exception("profile is private")
    