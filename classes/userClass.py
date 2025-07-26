from constants import STEAM_ID_LINK, GAME_TAGS_LINK
from bs4 import BeautifulSoup
import os



class User:
  def __init__(self, user_id, friend_list = [], game_list = [], is_account_private = True):
    self.user_id = user_id
    self.friend_list = friend_list
    self.game_list = game_list
    self.is_account_private = is_account_private

def check_privacy_setting(self, user_id, is_account_private): #check to see the privacy status of the user profile
    user_id_link = STEAM_ID_LINK + self.user_id

    with open(user_id_link) as fp:
      soup = BeautifulSoup(fp, 'html.parser')
    soup = BeautifulSoup(f"<html>{user_id_link}</html>", 'html.parser')
      
    info_table = soup.find("table", id = "profile-info")
    for child in info_table.contents:
      print(child)

  

def get_game_list(self, user_id, game_list, is_account_private):
  if self.is_account_private == True:   #return error and instructions to set your profile to public
    pass

def get_friend_list(self, user_id, friend_list, is_account_private):
  if self.is_account_private == True:   #return error and instructions to set your profile to public
    pass
    



def main():
  moogle = User("76561198053719898")


if __name__ == "__main__":
  main()
