import os
import sys
import requests

child_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(child_dir, '..'))
sys.path.append(parent_dir)
from constants import STEAM_ID_LINK, GAME_TAGS_LINK
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}




class User:
  def __init__(self, user_id, friend_list = [], game_list = [], is_account_private = True):
    self.user_id = user_id
    self.friend_list = friend_list
    self.game_list = game_list
    self.is_account_private = is_account_private

  def check_privacy_setting(self): #check to see the privacy status of the user profile
    user_id_link = STEAM_ID_LINK + self.user_id

    with requests.get(user_id_link, headers=headers) as response:
      soup = BeautifulSoup(response.text, 'html.parser')
      
    info_table = soup.find("table", id = "profile-info")
    for child in info_table.contents:
      print(child)

  

  def get_game_list(self):
    if self.is_account_private == True:   #return error and instructions to set your profile to public
      pass

  def get_friend_list(self):
    if self.is_account_private == True:   #return error and instructions to set your profile to public
      pass
    



def main():
  moogle = User("76561198053719898")
  moogle.check_privacy_setting()


if __name__ == "__main__":
  main()
