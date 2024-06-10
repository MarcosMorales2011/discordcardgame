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

"""
Spells
Laser Beam: 2 Cost, 2 Physics. On activation: enemy player takes 5 damage
Blue Shield Emitter: 3 Cost. On activation: Owner takes -2 damage from all sources

Traps
Important to note, trap cards dont trigger automatically. The owner should have the choice to trigger them or not when the condition is met
Anti-Personnel Mines: 3 Cost (trap cards are placed in the battlefield upside down). Trigger Condition: Player is attacked. Effect: All attacking creatures take 2 points of damage
Focused Artillery: 2 cost, 1 Physics. Trigger Condition: Player puts down a creature, Effect: Creature who just got put down take 6 damage

Artifacts
Laser Hangun, 2 Cost, Attachment Cost: 1, Gives target creature +3 damage
Cyno-Revival Chambers, 3 Cost, Attachment Cost: 2, When target creature dies, bring it to your hand instead of your graveyard (the artifact still goes to the graveyard)

Resources
Physics lab, 1 cost, on tap: gain +1 physics
Health lab, 1 cost, on tap: gain +1 health
"""
#Technologies(Spells)
laser_beam = Technologies(name="Laser Beam", attributes={}, cost={}, spell_effect={})
blue_shield_emitter= Technologies(name="Blue Shield Emitter", attributes={}, cost={}, spell_effect={})

#Traps
anti_personnel_mines=Trap(name="Anti-Personnel Mines", attributes={}, cost={}, trigger_condition="")
focused_artillery=Trap(name="Focused Artillery", attributes={}, cost={}, trigger_condition="")

#Equipment (Artifacts)
laser_handgun=Equipment(name="Laser Handgun", attributes={}, cost={}, attachment_cost={}, effects={})
cyno_revival_chambers=Equipment(name="Cyno-Revival Chambers", attributes={}, cost={}, attachment_cost={}, effects={})

#Resources
physics_lab=Resource(name="Physics Lab", attributes={}, amount=0, cost=0)
chemistry_lab=Resource(name="Chemistry Lab", attributes={}, amount=0, cost=0)



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