import random
from classes.gameClass import Game
from classes.stateClass import State
from classes.sessionClass import Session
from constants import *

# --- Helper Function for Test Data ---
def create_sample_games(num_games):
    games = []
    for i in range(num_games):
        # Using a fixed set of tags for simplicity
        tags = random.choice([["action"], ["adventure"], ["puzzle"], ["strategy"]])
        games.append(Game(app_id=i, name=f"Game {i+1}", tags=tags, hours=random.randint(10, 100)))
    return games

print("--- Starting Logic Test ---")

# --- Scenario 1: Basic flow with a moderate number of games ---
print("\n=== Scenario 1: Moderate Games, Confirming Selection ===")
sample_games_1 = create_sample_games(25) # More than UPPER_LIMIT, so max batch 10
session_1 = Session(sample_games_1)
print(f"Initial Current Batch Size: {session_1.current_batch_size}")
print(f"Initial History: {len(session_1.history_array)} states")
print(f"Initial Batch: {session_1.history_array[0].batch}")
print(f"Initial Remaining: {len(session_1.history_array[0].remaining_games)} games")

# Simulate selecting a few games in the first batch
print("\nSimulating selection in first batch...")
session_1.history_array[0].batch[0].switch_selection() # Select game 1
session_1.history_array[0].batch[2].switch_selection() # Select game 3
print(f"Selected Games in Batch: {[g.name for g in session_1.history_array[0].batch if g.is_selected]}")

session_1.confirm()
print(f"\nAfter first Confirm - History Array Length: {len(session_1.history_array)}")
current_state_1 = session_1.history_array[session_1.current_index]
print(f"Current Index: {session_1.current_index}")
print(f"New Batch: {current_state_1.batch}")
print(f"New Remaining: {len(current_state_1.remaining_games)} games")
print(f"New Seen Games: {current_state_1.seen_games}") # Should contain the selected games from previous batch

# --- Scenario 2: Testing Undo/Redo ---
print("\n=== Scenario 2: Testing Undo/Redo ===")
sample_games_2 = create_sample_games(15) # Example to get some batches
session_2 = Session(sample_games_2)
print(f"Session 2 Initial History: {len(session_2.history_array)} states")

# Confirm a few times without selection (to test confirm guard)
print("\nAttempting confirms without selection (shouldn't add states):")
session_2.confirm()
session_2.confirm()
print(f"History after no-selection confirms: {len(session_2.history_array)}") # Should still be 1

# Make a selection and confirm
print("\nMaking a selection and confirming (should add a state):")
session_2.history_array[session_2.current_index].batch[0].switch_selection()
session_2.confirm()
print(f"History after 1st real confirm: {len(session_2.history_array)}") # Should be 2

# Make another selection and confirm
session_2.history_array[session_2.current_index].batch[0].switch_selection()
session_2.confirm()
print(f"History after 2nd real confirm: {len(session_2.history_array)}") # Should be 3

print(f"\nBefore undo - current index: {session_2.current_index}")
session_2.undo()
print(f"After first undo - current index: {session_2.current_index}")
session_2.undo()
print(f"After second undo - current index: {session_2.current_index}")
session_2.undo() # Should not go below 0
print(f"After third undo (at 0) - current index: {session_2.current_index}")

print(f"\nBefore redo - current index: {session_2.current_index}")
session_2.redo()
print(f"After first redo - current index: {session_2.current_index}")
session_2.redo()
print(f"After second redo - current index: {session_2.current_index}")
session_2.redo() # Should not go beyond history_array length - 1
print(f"After third redo (at max) - current index: {session_2.current_index}")


# --- Scenario 3: Reaching Final Pick ---
print("\n=== Scenario 3: Reaching Final Pick ===")
# Create a small list of games to force MIN_BATCH rapidly
# Adjust this number based on your constants and how quickly you want to reach MIN_BATCH
sample_games_3 = create_sample_games(4) # e.g., if MIN_BATCH is 1, 4 games means a few steps
session_3 = Session(sample_games_3)
print(f"Initial Session 3 Current Batch Size: {session_3.current_batch_size}")
print(f"Initial Session 3 History: {len(session_3.history_array)} states")
print(f"Initial Session 3 Batch: {session_3.history_array[0].batch}")
print(f"Initial Session 3 Remaining Games: {len(session_3.history_array[0].remaining_games)}")
print(f"Initial Session 3 Seen Games: {len(session_3.history_array[0].seen_games)}")
print(f"Initial Session 3 Final Pick: {session_3.history_array[0].final_pick}")

step_count = 0
# Loop until the final_pick is set in the current state's batch
# or a safety limit is reached to prevent infinite loops during testing
while not session_3.history_array[session_3.current_index].final_pick and step_count < 20: # Safety limit 20 steps
    step_count += 1
    current_state_3 = session_3.history_array[session_3.current_index]

    print(f"\n--- Step {step_count} ---")
    print(f"Current Index: {session_3.current_index}")
    print(f"Session Current Batch Size (driving factor): {session_3.current_batch_size}") # This is the changing variable
    print(f"Current State Batch: {current_state_3.batch}")
    print(f"Current State Remaining Games: {len(current_state_3.remaining_games)}")
    print(f"Current State Seen Games: {len(current_state_3.seen_games)}")
    print(f"Is Final Pick Set in Current State: {current_state_3.final_pick is not None}")

    # Simulate selecting games to advance the state
    # To reliably reach the end, let's always select the first game in the batch
    # This ensures 'confirm' proceeds and the batch size can eventually shrink.
    if current_state_3.batch: # Only try to select if there are games in the batch
        current_state_3.batch[0].switch_selection() # Select the first game
        print(f"Simulating selection of: {current_state_3.batch[0].name}")
    else:
        print("Batch is empty, cannot simulate selection. This might indicate an issue.")
        break # Exit loop if batch is unexpectedly empty

    session_3.confirm()
    print(f"History Length after confirm: {len(session_3.history_array)}")

    # After the loop finishes, check the final state
print("\n--- Final State of Scenario 3 ---")
final_state_3 = session_3.history_array[session_3.current_index]
print(f"Final Current Index: {session_3.current_index}")
print(f"Final Session Current Batch Size: {session_3.current_batch_size}")
print(f"Final State Batch: {final_state_3.batch}")
print(f"Final State Remaining Games: {len(final_state_3.remaining_games)}")
print(f"Final State Seen Games: {len(final_state_3.seen_games)}") # This line completes the list of prints
print(f"Final State Final Pick: {final_state_3.final_pick}")

# You might want to add assertions here if using a proper testing framework
# For example:
# assert final_state_3.final_pick is not None, "Final pick should be set!"
# assert len(final_state_3.batch) == 1, "Final batch should contain only one game!"

print("\n=== Scenario 3 Test Complete ===")

