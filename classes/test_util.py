import unittest

from utilityClass import *

class TestTextNode(unittest.TestCase):
    def test_find_common_games_3(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_3 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("bob", "123", None, games_1, False), User("sob", "321", None, games_2, False), User("lob", "456", None, games_3, False)]
        main_user = User("super bob", "333", None, games_1, False)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]))
            
    def test_find_common_games_1(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = [Game(12345, "Counter-Strike", None, 0), Game(621, "hog warts", None, 0)]
        games_3 = [Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("bob", "123", None, games_1, False), User("sob", "321", None, games_2, False), User("lob", "456", None, games_3, False)]
        main_user = User("super bob", "333", None, games_1, False)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(621, "hog warts", None, 0)]))
        
    def test_find_common_games_empty_user(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = []
        games_3 = [Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("bob", "123", None, games_1, False), User("sob", "321", None, games_2, False), User("lob", "456", None, games_3, False)]
        main_user = User("super bob", "333", None, games_1, False)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]))
        

if __name__ == "__main__":
    unittest.main()