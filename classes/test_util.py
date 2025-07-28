import unittest

from utilityClass import *

class TestTextNode(unittest.TestCase):
    def test_find_common_games_3(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_3 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("123","bob", games_1), User("321","sob", games_2), User("456","lob", games_3)]
        main_user = User("852","super bob", games_1)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]))
            
    def test_find_common_games_1(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = [Game(12345, "Counter-Strike", None, 0), Game(621, "hog warts", None, 0)]
        games_3 = [Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("123","bob", games_1), User("321","sob", games_2), User("456","lob", games_3)]
        main_user = User("852","super bob", games_1)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(621, "hog warts", None, 0)]))
        
    def test_find_common_games_empty_user(self):
        games_1 = [Game(12345, "Counter-Strike", None, 0), Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        games_2 = []
        games_3 = [Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]
        user_list = [User("123","bob", games_1), User("321","sob", games_2), User("456","lob", games_3)]
        main_user = User("852","super bob", games_1)
        common_games = Utility.find_common_games(main_user, user_list)
        self.assertEqual(set(common_games), set([Game(45678, "Minecraft", None, 0), Game(621, "hog warts", None, 0)]))

class TestReduceGamesListFromTags(unittest.TestCase):

    def setUp(self):
        """Set up common test data (Game objects) before each test method."""
        # Define some sample games with various tags
        self.game_action_rpg = Game(1, "Epic Quest", ["action", "RPG"], 50)
        self.game_puzzle_adventure = Game(2, "Mystery Maze", ["puzzle", "adventure"], 20)
        self.game_strategy = Game(3, "War Tactics", ["strategy"], 80)
        self.game_indie_action = Game(4, "Pixel Fury", ["indie", "action"], 15)
        self.game_rpg_only = Game(5, "Fantasy Saga", ["RPG"], 100)
        self.game_no_tags = Game(6, "Zen Garden", [], 5) # Game with no tags

        self.all_sample_games = [self.game_action_rpg,
                                 self.game_puzzle_adventure,
                                 self.game_strategy,
                                 self.game_indie_action,
                                 self.game_rpg_only,
                                 self.game_no_tags]

    # --- Test Cases for Valid Inputs ---

    def test_single_tag_match(self):
        """Test filtering with a single tag that matches some games (AND logic trivial)."""
        filtering_tags = ["action"]
        expected_games = [self.game_action_rpg, self.game_indie_action]
        
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertCountEqual(result, expected_games, "Should return games tagged 'action'.")

    def test_multiple_tags_all_must_match(self):
        """
        Test filtering with multiple tags where a game is included only if ALL tags match.
        Verifies that games are unique in the output.
        """
        filtering_tags = ["action", "RPG"] # Only game_action_rpg has BOTH "action" and "RPG"
        expected_games = [self.game_action_rpg] # game_action_rpg is the only one
        
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertCountEqual(result, expected_games, "Should return only games matching ALL specified tags.")

    def test_multiple_tags_no_game_matches_all(self):
        """
        Test filtering with multiple tags where no single game possesses ALL of them,
        even if individual tags are present in different games.
        """
        filtering_tags = ["strategy", "action"] # game_strategy has "strategy", others have "action" but no single game has both
        expected_games = []
        
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertEqual(result, expected_games, "Should return an empty list if no game matches ALL tags.")

    def test_no_matching_tags(self):
        """Test filtering with tags that don't match any games."""
        filtering_tags = ["horror", "simulation"]
        expected_games = []
        
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertEqual(result, expected_games, "Should return an empty list if no tags match.")

    def test_empty_filtering_tags(self):
        """Test when filtering_tags list is empty (should return original list)."""
        filtering_tags = []
        
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertListEqual(result, self.all_sample_games, 
                              "Should return the exact original list if filtering_tags is empty.")

    def test_game_with_no_tags(self):
        """Test how games with empty tags list are handled (should not be included unless filter is empty)."""
        filtering_tags = ["action"]
        # game_no_tags has no tags, so it shouldn't be included as it can't match "action"
        expected_games = [self.game_action_rpg, self.game_indie_action]
        result = Utility.reduce_games_list_from_tags(filtering_tags, self.all_sample_games)
        self.assertCountEqual(result, expected_games, "Games with no tags should not match any filter.")

    # --- Test Cases for Invalid Inputs (Error Handling) ---

    def test_list_of_games_not_list(self):
        """Test that TypeError is raised if list_of_games is not a list."""
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_tags(["tag"], "not a list")
        self.assertIn("Input 'list_of_games' in Utility.reduce_games_list_from_tags must be a list.", str(cm.exception))

    def test_list_of_games_empty(self):
        """Test that ValueError is raised if list_of_games is empty."""
        with self.assertRaises(ValueError) as cm:
            Utility.reduce_games_list_from_tags(["tag"], [])
        self.assertIn("The 'list_of_games' is empty.", str(cm.exception))

    def test_list_of_games_contains_non_game_object(self):
        """Test that TypeError is raised if list_of_games contains non-Game objects."""
        invalid_list = [self.game_action_rpg, "not a game", self.game_strategy]
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_tags(["tag"], invalid_list)
        self.assertIn("All elements in 'list_of_games' in Utility.reduce_games_list_from_tags must be instances of the Game class.", str(cm.exception))

    def test_filtering_tags_not_list(self):
        """Test that TypeError is raised if filtering_tags is not a list."""
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_tags("not a list", self.all_sample_games)
        self.assertIn("Input 'filtering_tags' in Utility.reduce_games_list_from_tags must be a list.", str(cm.exception))

    def test_filtering_tags_contains_non_string(self):
        """Test that TypeError is raised if filtering_tags contains non-string elements."""
        invalid_tags = ["action", 123, "strategy"] # 123 is not a string
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_tags(invalid_tags, self.all_sample_games)
        self.assertIn("All elements in 'filtering_tags' in Utility.reduce_games_list_from_tags must be strings.", str(cm.exception))

class TestReduceGamesListFromHours(unittest.TestCase):

    def setUp(self):
        """Set up common test data (Game objects) before each test method."""
        # Define some sample games with various hours played
        self.game_short = Game(1, "Quick Play", ["casual"], 5.0)
        self.game_medium = Game(2, "Mid-Core Adventure", ["adventure"], 25.5)
        self.game_long = Game(3, "Epic Saga", ["RPG"], 150.0)
        self.game_zero_hours = Game(4, "Unplayed Gem", ["puzzle"], 0.0)
        self.game_just_right = Game(5, "Perfect Fit", ["action"], 10.0)

        self.all_sample_games = [self.game_short,
                                 self.game_medium,
                                 self.game_long,
                                 self.game_zero_hours,
                                 self.game_just_right]

    # --- Test Cases for Valid Inputs ---

    def test_filter_some_games(self):
        """Test filtering with a threshold that includes some games."""
        hours_threshold = 30.0
        # Expected: games with hours <= 30.0
        # game_short (5.0), game_medium (25.5), game_zero_hours (0.0), game_just_right (10.0)
        expected_games = [self.game_short,
                          self.game_medium,
                          self.game_zero_hours,
                          self.game_just_right]
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        # assertCountEqual is good as order might not be strictly preserved by the filter
        self.assertCountEqual(result, expected_games, "Should return games within the hours threshold.")

    def test_filter_no_games(self):
        """Test filtering with a very low threshold that excludes all games (except maybe 0-hour ones)."""
        hours_threshold = -1.0 # No game can have negative hours
        expected_games = []
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        self.assertEqual(result, expected_games, "Should return an empty list if no games meet the criteria.")

    def test_filter_all_games(self):
        """Test filtering with a very high threshold that includes all games."""
        hours_threshold = 200.0 # All sample games are less than 200 hours
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        # Your function doesn't change the order of the original list if all games pass
        self.assertListEqual(result, self.all_sample_games, "Should return all original games if threshold is very high.")

    def test_hours_is_none(self):
        """Test when 'hours' parameter is None (should return original list)."""
        hours_threshold = None
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        self.assertListEqual(result, self.all_sample_games, "Should return original list if hours is None.")

    def test_hours_is_integer(self):
        """Test when 'hours' parameter is an integer (should be converted to float)."""
        hours_threshold = 10 # This should be treated as 10.0
        expected_games = [self.game_short,      # 5.0 <= 10.0
                          self.game_zero_hours, # 0.0 <= 10.0
                          self.game_just_right]  # 10.0 <= 10.0
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        self.assertCountEqual(result, expected_games, "Should correctly filter when hours is an integer.")

    def test_hours_is_zero(self):
        """Test filtering with a 0-hour threshold."""
        hours_threshold = 0.0
        expected_games = [self.game_zero_hours] # Only the game with 0.0 hours
        
        result = Utility.reduce_games_list_from_hours(hours_threshold, self.all_sample_games)
        self.assertCountEqual(result, expected_games, "Should filter correctly for 0.0 hours.")

    # --- Test Cases for Invalid Inputs (Error Handling) ---

    def test_list_of_games_not_list(self):
        """Test that TypeError is raised if list_of_games is not a list."""
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_hours(10.0, "not a list")
        self.assertIn("Input 'list_of_games' in Utility.reduce_games_list_from_hours must be a list.", str(cm.exception))

    def test_list_of_games_empty(self):
        """Test that ValueError is raised if list_of_games is empty."""
        with self.assertRaises(ValueError) as cm:
            Utility.reduce_games_list_from_hours(10.0, [])
        self.assertIn("The 'list_of_games' is empty.", str(cm.exception))

    def test_list_of_games_contains_non_game_object(self):
        """Test that TypeError is raised if list_of_games contains non-Game objects."""
        invalid_list = [self.game_short, "not a game", self.game_long]
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_hours(10.0, invalid_list)
        self.assertIn("All elements in 'list_of_games' in Utility.reduce_games_list_from_hours must be instances of the Game class.", str(cm.exception))

    def test_hours_not_float_or_int(self):
        """Test that TypeError is raised if 'hours' is not a float or int."""
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_hours("ten", self.all_sample_games) # Pass a string
        self.assertIn("Input 'hours' in Utility.reduce_games_list_from_hours must be a float, but instead it's a", str(cm.exception))
        
        with self.assertRaises(TypeError) as cm:
            Utility.reduce_games_list_from_hours(True, self.all_sample_games) # Pass a boolean
        self.assertIn("Input 'hours' in Utility.reduce_games_list_from_hours must be a float, but instead it's a", str(cm.exception))

class TestGetAllTagsFromGamesList(unittest.TestCase):

    def setUp(self):
        """Set up common test data (Game objects) before each test method."""
        # Define some sample games with various tags
        self.game1 = Game(1, "Game A", ["action", "RPG"])
        self.game2 = Game(2, "Game B", ["adventure", "puzzle"])
        self.game3 = Game(3, "Game C", ["action", "strategy"])
        self.game4 = Game(4, "Game D", ["RPG", "indie"])
        self.game5 = Game(5, "Game E", ["casual"])
        self.game_no_tags_empty = Game(6, "Game F", []) # Game with an empty tags list
        self.game_no_tags_none = Game(7, "Game G", None) # Game with None for tags

        self.all_sample_games = [self.game1,
                                 self.game2,
                                 self.game3,
                                 self.game4, 
                                 self.game5,
                                 self.game_no_tags_empty,
                                 self.game_no_tags_none]

    # --- Test Cases for Valid Inputs ---

    def test_basic_tag_extraction(self):
        """Test with a standard list of games, ensuring all unique tags are extracted and sorted."""
        expected_tags = ["action", "adventure", "casual", "indie", "puzzle", "RPG", "strategy"]
        result = Utility.get_all_tags_from_games_list(self.all_sample_games)
        self.assertEqual(result, expected_tags, "Should extract all unique tags and sort them alphabetically.")

    def test_games_with_overlapping_tags(self):
        """Test that overlapping tags (e.g., 'action' in multiple games) result in unique output."""
        # Only use games that have 'action' in them
        games_subset = [self.game1, self.game3] # Both have "action"
        expected_tags = ["action", "RPG", "strategy"]
        result = Utility.get_all_tags_from_games_list(games_subset)
        self.assertEqual(result, expected_tags, "Should correctly deduplicate tags from multiple games.")

    def test_games_with_no_tags_included(self):
        """Test that games with empty or None tags lists do not contribute to the tags."""
        # A list containing only games with no tags
        games_only_no_tags = [self.game_no_tags_empty, self.game_no_tags_none]
        expected_tags = []
        result = Utility.get_all_tags_from_games_list(games_only_no_tags)
        self.assertEqual(result, expected_tags, "Should return an empty list if games have no tags.")
        
        # Test with a mix, ensuring they don't add
        games_mix = [self.game5, self.game_no_tags_empty, self.game_no_tags_none]
        expected_tags_mix = ["casual"]
        result_mix = Utility.get_all_tags_from_games_list(games_mix)
        self.assertEqual(result_mix, expected_tags_mix, "Games with no tags should not add to the list of tags.")


    def test_empty_list_of_games_raises_error(self):
        """Test that ValueError is raised if list_of_games is empty."""
        with self.assertRaises(ValueError) as cm:
            Utility.get_all_tags_from_games_list([])
        self.assertIn("The 'list_of_games' is empty.", str(cm.exception))

    # --- Test Cases for Invalid Inputs (Error Handling) ---

    def test_list_of_games_not_list(self):
        """Test that TypeError is raised if list_of_games is not a list."""
        with self.assertRaises(TypeError) as cm:
            Utility.get_all_tags_from_games_list("not a list")
        self.assertIn("Input 'list_of_games' in Utility.get_all_tags_from_games_list must be a list.", str(cm.exception))

    def test_list_of_games_contains_non_game_object(self):
        """Test that TypeError is raised if list_of_games contains non-Game objects."""
        invalid_list = [self.game1, "not a game", self.game3]
        with self.assertRaises(TypeError) as cm:
            Utility.get_all_tags_from_games_list(invalid_list)
        self.assertIn("All elements in 'list_of_games' in Utility.get_all_tags_from_games_list must be instances of the Game class.", str(cm.exception))

if __name__ == "__main__":
    unittest.main()