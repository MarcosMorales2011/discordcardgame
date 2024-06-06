from typing import List
from Card import Card
from Player import Player
import random

class Gamestate:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.current_player, self.opponent = self.determine_first_player()
        self.phase = 'Untap'
        self.turn_counter = 1

    def determine_first_player(self):
        """Randomly determine which player goes first."""
        players = [self.player1, self.player2]
        random.shuffle(players)
        print(f"{players[0].name} will go first.")
        return players[0], players[1]

    def next_phase(self):
        """Progress to the next phase in the turn cycle."""
        phases = ['Untap', 'Upkeep', 'Draw', 'Main1', 'Combat', 'Main2', 'End']
        current_index = phases.index(self.phase)
        self.phase = phases[(current_index + 1) % len(phases)]
        print(f"Transitioned to {self.phase} phase.")

    def switch_player(self):
        """Switch the current player to the opponent."""
        self.current_player, self.opponent = self.opponent, self.current_player
        self.current_player.reset_land_played()
        print(f"It is now {self.current_player.name}'s turn.")
        
        if self.turn_counter % 2 == 0:
            self.current_player.increase_mana()
            self.opponent.increase_mana()
        
        self.turn_counter += 1

    def untap_phase(self):
        """Handle the Untap phase."""
        for card in self.current_player.battlefield:
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
        if phase_num == 1:
            print("Entering Main Phase 1.")
        else:
            print("Entering Main Phase 2.")
            
        # Allow the player to perform any legal actions such as playing lands, casting spells, or activating abilities
        self.perform_actions()
        self.next_phase()

    def perform_actions(self):
        print(f"{self.current_player.name} can perform actions now.")
        # Placeholder for actual game logic to perform actions
        # This should be replaced with the actual logic for player actions

    def combat_phase(self):
        """Handle the Combat phase."""
        print("Entering Combat Phase.")
        attackers = self.select_attackers()
        if attackers:
            self.declare_attackers(attackers)
        self.next_phase()

    def select_attackers(self) -> List[Card]:
        """Select attackers from the current player's battlefield."""
        print(f"{self.current_player.name}, select attackers for combat:")
        print("Your Battlefield:")
        for index, card in enumerate(self.current_player.battlefield, start=1):
            print(f"{index}. {card} ({card.card_type})")
        
        selected_attackers = []
        while True:
            try:
                selection = input("Enter the number of the card to attack with (0 to finish selecting): ")
                index = int(selection) - 1
                if index == -1:
                    break
                selected_attackers.append(self.current_player.battlefield[index])
                print(f"{self.current_player.battlefield[index].name} selected as an attacker.")
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a valid number.")

        return selected_attackers

    def declare_attackers(self, attackers: List[Card]):
        """Handle the Declare Attackers step."""
        print(f"{self.current_player.name} is declaring attackers.")
        total_attack = 0
        for attacker in attackers:
            if attacker in self.current_player.battlefield:
                print(f"{attacker.name} is attacking with {attacker.attributes['attack']} attack.")
                total_attack += attacker.attributes['attack']
            else:
                print(f"{attacker.name} is not on the battlefield and cannot attack.")
        self.damage_enemy_player(total_attack)

    def damage_enemy_player(self, attack_points: int):
        self.opponent.take_damage(attack_points)
        print(f"{self.opponent.name} took {attack_points} damage.")

    def end_phase(self):
        """Handle the End phase."""
        self.end_step()
        self.cleanup_step()
        self.switch_player()
        self.next_phase()

    def end_step(self):
        """Handle the End Step."""
        print("End Step: resolving end-of-turn effects.")

    def cleanup_step(self):
        """Handle the Cleanup Step."""
        self.current_player.hand.cleanup()
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
        """Check if the game has been won."""
        if self.player1.hp <= 0 or self.player2.hp <= 0:
            winner = self.player1 if self.player2.hp <= 0 else self.player2
            print(f"{winner.name} wins the game!")
            return True
        return False