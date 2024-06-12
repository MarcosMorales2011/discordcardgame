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
        for card in self.current_player.battlefield:
            if card.card_type == "Resource":
                card.untap()
                self.current_player.untap_resource()
            else:
                card.untap()
        self.next_phase()

    def upkeep_phase(self):
        """Handle the Upkeep phase."""
        for card in self.current_player.battlefield:
            self.trigger_upkeep(self.current_player, card)  
            print(card.card_type)
        self.next_phase()

    def trigger_upkeep(self, player, card):
        """
        Trigger the upkeep ability and handle upkeep costs for a card.
        
        :param player: The player who controls the card.
        :param card: The card with an upkeep trigger.
        """
        if card.upkeep_cost:
            can_pay = player.use_mana(card.upkeep_cost)
            if not can_pay:
                print(f"{player.name} cannot pay the upkeep cost for {card.name}. Taking consequences.")
                # Handle consequences here (e.g., sacrifice the card)
        if card.upkeep_ability:
            card.upkeep_ability(player, card)

    def draw_phase(self):
        """Handle the Draw phase."""
        if self.turn_counter == 1 or 2:
            self.current_player.hand.draw_initial_hand(self.current_player.deck)
        else:
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
        self.current_player.hand.view_hand()
        action_taken = False

        while not action_taken:
            print(f"Your Common Mana: {self.current_player.get_common_mana()}")
            print(f"Your Resource Pool: {self.current_player.get_resource_pool()}")
            action = input(f"{self.current_player.name}, choose an action (play/attach/activate/skip): ").strip().lower()

            if action == "skip":
                print(f"{self.current_player.name} skips their main phase.")
                action_taken = True

            elif action == "play":
                self.current_player.hand.view_hand()
                card_name = input("Enter the name of the card you want to play: ").strip()

                card = self.current_player.hand.place_card(card_name)
                if card:
                    if card.card_type == "Resource" and self.current_player.land_played:
                        print(f"{self.current_player.name} cannot play another land this turn.")
                        self.current_player.hand.cards.append(card)  # Return card to hand
                    elif card.card_type == "Equipment" and card.attributes.get("Attach", True):
                        print(f"{self.current_player.name} cannot play {card_name} directly. It must be attached to a creature.")
                        self.current_player.hand.cards.append(card)  # Return card to hand
                    else:
                        if self.current_player.can_pay_cost(card.cost):
                            self.current_player.pay_cost(card.cost)
                            if card.card_type == "Resource":
                                self.current_player.land_played = True
                                for resource_type, amount in card.attributes.items():
                                    self.current_player.resource_pool[resource_type] += amount
                            self.current_player.battlefield.append(card)
                            if card.card_type == "Trap":
                                self.current_player.traps.append(card)  # Add the trap to the player's traps list
                            print(f"{self.current_player.name} placed {card} onto the battlefield.")
                            action_taken = True
                            self.check_traps("Opponent Card Placed", card)
                        else:
                            print(f"{self.current_player.name} cannot pay the cost for {card_name}.")
                            self.current_player.hand.cards.append(card)  # Return card to hand
                else:
                    print(f"{self.current_player.name} could not find {card_name} in hand to play.")


            elif action == "attach":
                self.current_player.hand.view_hand()
                equipment_name = input("Enter the name of the equipment to attach: ").strip()
                equipment = self.current_player.hand.place_card(equipment_name)

                if equipment and equipment.card_type == "Equipment":
                    if self.current_player.can_pay_cost(equipment.cost):
                        self.current_player.get_battlefield()
                        target_name = input("Enter the name of the creature to attach it to: ").strip()
                        target_creature = next((card for card in self.current_player.battlefield if card.name == target_name), None)
                        if target_creature:
                            self.current_player.pay_cost(equipment.cost)
                            self.current_player.attach_equipment(equipment, target_creature)
                            action_taken = True
                        else:
                            print(f"{target_name} is not on the battlefield.")
                            self.current_player.hand.cards.append(equipment)  # Return equipment to hand
                    else:
                        print(f"{self.current_player.name} could not find {equipment_name} in hand to attach or cannot pay the cost.")
                        if equipment:
                            self.current_player.hand.cards.append(equipment)  # Return equipment to hand
                else: 
                    print(f"{self.current_player.name} could not find {equipment_name} in hand to activate or it is not a Equipment card.")
                    if equipment:
                        self.current_player.hand.cards.append(technology)

            elif action == "activate":
                self.current_player.hand.view_hand()
                technology_name = input("Enter the name of the technology to activate: ").strip()
                technology = self.current_player.hand.place_card(technology_name)

                if technology and technology.card_type == "Technology":
                    if self.current_player.can_pay_cost(technology.cost):
                        self.current_player.pay_cost(technology.cost)
                        self.current_player.activate_technology(technology, self)
                        action_taken = True
                    else:
                        print(f"{self.current_player.name} cannot pay the cost for {technology_name}.")
                        self.current_player.hand.cards.append(technology)  # Return technology to hand
                else:
                    print(f"{self.current_player.name} could not find {technology_name} in hand to activate or it is not a Technology card.")
                    if technology:
                        self.current_player.hand.cards.append(technology)  # Return technology to hand

            else:
                print("Invalid action. Please try again.")



    def can_pay_cost(self, cost):
        """
        Check if the player can pay the cost.
        """
        for resource, amount in cost.items():
            if self.current_player.resource_pool.get(resource, 0) < amount:
                return False
        return True


    def combat_phase(self):
        """Handle the Combat phase."""
        print("Entering Combat Phase.")
        attackers = self.select_attackers()
        if attackers.__len__() != 0:
            self.declare_attackers(attackers)
        self.next_phase()

    def select_attackers(self) -> List[Card]:
        """Select attackers from the current player's battlefield."""
        print(f"{self.current_player.name}, select attackers for combat:")
        print("Your Battlefield:")

        valid_attackers = [card for card in self.current_player.battlefield if card.card_type == "Creature"]
        for index, card in enumerate(valid_attackers, start=1):
            print(f"{index}. {card.name} ({card.card_type}) - Attack: {card.attributes['attack']}")

        selected_attackers = []
        while True:
            try:
                selection = input("Enter the number of the card to attack with (0 to finish selecting): ")
                index = int(selection) - 1
                if index == -1:
                    break
                if 0 <= index < len(valid_attackers):
                    selected_attackers.append(valid_attackers[index])
                    print(f"{valid_attackers[index].name} selected as an attacker.")
                else:
                    print("Invalid selection. Please enter a valid number.")
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a valid number.")

        return selected_attackers

    def declare_attackers(self, attackers: List[Card]):
        """Handle the Declare Attackers step."""
        print(f"{self.current_player.name} is declaring attackers.")
        total_attack = 0
        for attacker in attackers:
            attacker.tap()
            if attacker in self.current_player.battlefield:
                print(f"{attacker.name} is attacking with {attacker.attributes['attack']} attack.")
                total_attack += attacker.attributes['attack']
            else:
                print(f"{attacker.name} is not on the battlefield and cannot attack.")
        self.damage_enemy_player(total_attack)

    def damage_enemy_player(self, attack_points: int):
        self.opponent.take_damage(attack_points)
        print(f"{self.opponent.name} took {attack_points} damage.")
        self.check_traps("Damage Dealt", attack_points)

    def end_phase(self):
        """Handle the End phase."""
        self.end_step()
        self.cleanup_step()
        self.switch_player()
        self.next_phase()

    def end_step(self):
        """Handle the End Step."""
        print("End Step: resolving end-of-turn effects.")
        # Handle end-of-turn effects here

    def cleanup_step(self):
        """Handle the Cleanup Step."""
        print("Cleanup Step: discarding excess cards and removing damage.")

        # Discard excess cards if hand size exceeds maximum (normally seven)
        max_hand_size = 7
        if self.current_player.hand.count() > max_hand_size:
            excess_cards = self.current_player.hand.count() - max_hand_size
            print(f"{self.current_player.name} has {excess_cards} excess cards.")
            self.current_player.hand.discard_excess(max_hand_size, self.current_player.hand.choose_discard())


        # Remove all damage marked on permanents
        for card in self.current_player.battlefield:
            if hasattr(card, "damage"):
                card.damage = 0  # Reset damage to 0
                print(f"Removed damage from {card.name}.")

        # End all "until end of turn" and "this turn" effects
        for card in self.current_player.battlefield:
            if hasattr(card, "end_turn_effects"):
                card.end_turn_effects.clear()  # Clear end turn effects
                print(f"Cleared end-of-turn effects from {card.name}.")

        # Check for state-based actions or triggered abilities
        self.check_state_based_actions_and_triggered_abilities()


    def check_state_based_actions_and_triggered_abilities(self):
        """Check for state-based actions or triggered abilities and handle them."""
        # Placeholder for checking state-based actions and triggered abilities
        # If any, put them on the stack and handle priority
        print("Checking for state-based actions and triggered abilities.")
        # This can be implemented with more details as needed

    def check_traps(self, condition, trigger):
        """Check and handle trap cards."""
        for trap in self.opponent.traps:
            if trap.condition == condition and trap.check_condition(trigger):
                print(f"{self.opponent.name} can activate {trap.name}.")
                activate = input(f"Do you want to activate {trap.name}? (yes/no): ").strip().lower()
                if activate == "yes":
                    trap.activate(self.opponent, self.current_player, self)

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