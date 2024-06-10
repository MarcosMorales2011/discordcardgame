from Player import *
from Deck import *
from Card import *
from Gamestate import *

# Create example players with decks
deck1 = Deck()
deck2 = Deck()

# Add example cards to the decks
fire_elemental = Creature(name="Fire Elemental", attributes={"attack": 6, "defense": 4, "alive": True, "race": "Elemental" }, cost={"Common": 3}, hp=5)
holy_elemental = Creature(name="Holy Angel", attributes={"attack": 2, "defense": 1, "alive": True, "race": "Angel"}, cost={"Common": 1}, hp=5)

# Try making 2 cards of every type. For now make each deck a random collection of these 10 cards. Then pint the decks.

for x in range(40):
    deck2.add_card(fire_elemental)
    deck1.add_card(holy_elemental)

# Create players
player1 = Player(name="Alice", discord_id=12345, deck=deck1)
player2 = Player(name="Bob", discord_id=67890, deck=deck2)

#Shuffling hands/decks.
player1.hand.shuffle()
player2.hand.shuffle()

# Initialize the game state
game_state = Gamestate(player1, player2)

# Start the game
game_state.start_game()