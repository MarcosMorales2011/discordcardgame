from Deck import Deck
from Hand import Hand
from Card import Card
from Player import Player
from typing import Optional

class GameState:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1  # Assuming player1 starts
        self.opponent = self.player2 if self.current_player == self.player1 else self.player1
        self.phase = 'Untap'

    def next_phase(self):
        """Progress to the next phase in the turn cycle."""
        phases = ['Untap', 'Upkeep', 'Draw', 'Main1', 'Combat', 'Main2', 'End']
        current_index = phases.index(self.phase)
        self.phase = phases[(current_index + 1) % len(phases)]
        if self.phase == 'Untap':
            self.switch_player()
        print(f"Transitioned to {self.phase} phase.")

    def switch_player(self):
        """Switch the current player to the opponent."""
        self.current_player, self.opponent = self.opponent, self.current_player
        print(f"It is now {self.current_player.name}'s turn.")

    def untap_phase(self):
        """Handle the Untap phase."""
        for card in self.current_player.battlefield:  # Assuming a battlefield attribute
            card.untap()  # Assuming an untap method in Card
        self.next_phase()

    def upkeep_phase(self):
        """Handle the Upkeep phase."""
        for card in self.current_player.battlefield:
            card.trigger_upkeep()  # Assuming a trigger_upkeep method in Card
        self.next_phase()

    def draw_phase(self):
        """Handle the Draw phase."""
        self.current_player.hand.draw_card(self.current_player.deck)
        self.next_phase()

    def main_phase(self, phase_num: int):
        """Handle the Main phase (either Main1 or Main2)."""
        # Allow the current player to play lands, cast spells, and activate abilities
        if phase_num == 1:
            print("Entering Main Phase")
        else:
            print("Entering Main Phase 2.")
        # Implement logic to allow the player to perform actions
        self.next_phase()

    def combat_phase(self):
        """Handle the Combat phase."""
        # Sequence for combat phase: declare attackers, declare blockers, deal damage, end of combat
        print("Entering Combat Phase.")
        self.declare_attackers()
        self.declare_blockers()
        self.deal_combat_damage()
        self.end_combat()
        self.next_phase()

    def declare_attackers(self):
        """Handle the Declare Attackers step."""
        # Implement logic for declaring attackers
        print(f"{self.current_player.name} is declaring attackers.")

    def declare_blockers(self):
        """Handle the Declare Blockers step."""
        # Implement logic for declaring blockers
        print(f"{self.opponent.name} is declaring blockers.")

    def deal_combat_damage(self):
        """Handle the Combat Damage step."""
        # Implement logic for dealing combat damage
        print("Dealing combat damage.")

    def end_combat(self):
        """Handle the End of Combat step."""
        # Implement logic for end of combat actions
        print("End of combat.")

    def end_phase(self):
        """Handle the End phase."""
        self.end_step()
        self.cleanup_step()
        self.next_phase()

    def end_step(self):
        """Handle the End Step."""
        # Implement logic for end step effects
        print("End Step: resolving end-of-turn effects.")

    def cleanup_step(self):
        """Handle the Cleanup Step."""
        self.current_player.hand.cleanup()
        # Implement logic for discarding down to maximum hand size and removing damage
        print("Cleanup Step: discarding excess cards and removing damage.")

    def play_turn(self):
        """Play a complete turn for the current player."""
        print(f"Starting {self.current_player.name}'s turn.")
        self.untap_phase()
        self.upkeep_phase()
        self.draw_phase()
        self.main_phase(1)
        self.combat_phase()
        self.main_phase(2)
        self.end_phase()

    def start_game(self):
        """Start the game and manage the flow of turns."""
        while not self.check_win_condition():
            self.play_turn()

    def check_win_condition(self) -> bool:
        if self.player1.hp <= 0 or self.player2.hp <= 0:
            winner = self.player1 if self.player2.hp <= 0 else self.player2
            print(f"{winner.name} wins the game!")
            return True
        return False

# Example usage:
if __name__ == "__main__":
    # Create example players with decks
    deck1 = Deck()
    deck2 = Deck()
    player1 = Player(name="Alice", deck=deck1)
    player2 = Player(name="Bob", deck=deck2)

    # Add example cards to the decks
    card1 = Card(name="Fire Elemental", card_type="Creature", attributes={"attack": 5, "defense": 4})
    card2 = Card(name="Healing Potion", card_type="Spell", attributes={"heal": 10})
    player1.deck.add_card(card1)
    player2.deck.add_card(card2)

    # Initialize the game state
    game_state = GameState(player1, player2)

    # Start the game
    game_state.start_game()