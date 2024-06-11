from Hand import Hand
from Deck import Deck
from typing import List, Dict
from Card import *

class Player:
    def __init__(self, name: str, discord_id: int, deck: Deck):
        self.name = name
        self.discord_id = discord_id
        self.deck = deck
        self.hand = Hand()
        self.battlefield: List[Card] = []
        self.hp = 40
        self.land_played = False
        self.mana = 1
        self.max_mana = 10
        self.graveyard = []
        self.resource_pool = {"Biology": 0, "Chemistry": 0, "Physics": 0, "Robotics": 0}
        self.damage_reduction = 0

    def reset_damage_reduction(self):
        self.damage_reduction = 0
    
    def take_damage(self, damage: int):
        self.hp -= damage-self.damage_reduction
        print(f"{self.name} takes {damage-self.damage_reduction} damage and is now at {self.hp} HP.")

    def heal(self, amount: int):
        self.hp += amount
        print(f"{self.name} heals {amount} and is now at {self.hp} HP.")

    def play_card_to_battlefield(self, card_name: str):
        card = self.hand.place_card(card_name)
        if card:
            if card.card_type == "Resource" and self.land_played:
                print(f"{self.name} cannot play another land this turn.")
            else:
                if card.card_type == "Resource":
                    self.land_played = True
                    for resource_type, amount in card.attributes.items():
                        self.resource_pool[resource_type] += amount
                self.battlefield.append(card)
                print(f"{self.name} placed {card} onto the battlefield.")
        else:
            print(f"{self.name} could not find {card_name} in hand to play.")

    def attach_equipment(self, equipment_name: str, target_creature: Card):
        equipment = self.hand.place_card(equipment_name)
        if equipment and isinstance(equipment, Equipment):
            if equipment.cost <= self.mana_pool:
                self.mana_pool -= equipment.cost
                target_creature.attributes['attack'] += equipment.effects.get('attack', 0)
                target_creature.attributes['defense'] += equipment.effects.get('defense', 0)
                print(f"{equipment.name} attached to {target_creature.name}, giving it {equipment.effects}.")
            else:
                print(f"Not enough mana to attach {equipment.name}.")
                self.hand.cards.append(equipment)  # Return the card to hand

    def use_equipment_on_self(self, equipment_name: str):
        equipment = self.hand.place_card(equipment_name)
        if equipment and isinstance(equipment, Equipment):
            if equipment.cost <= self.mana_pool:
                self.mana_pool -= equipment.cost
                self.apply_effects(equipment.effects)
                if equipment.single_use:
                    self.graveyard.append(equipment)
                    print(f"{equipment.name} used on {self.name}, applying effects {equipment.effects}. Moved to graveyard.")
            else:
                print(f"Not enough mana to use {equipment.name}.")
                self.hand.cards.append(equipment)  # Return the card to hand

    def apply_effects(self, effects: dict):
        if 'heal' in effects:
            self.hp += effects['heal']
            print(f"{self.name} heals for {effects['heal']} HP.")

    def activate_technology(self, technology_name: str, game_state):
        technology = self.hand.place_card(technology_name)
        if technology and isinstance(technology, Technologies):
            if technology.cost['mana'] <= self.mana_pool:
                self.mana_pool -= technology.cost['mana']
                self.resolve_technology_effect(technology, game_state)
                if technology.single_use:
                    self.graveyard.append(technology)
                    print(f"{technology.name} activated and moved to graveyard.")
            else:
                print(f"Not enough mana to activate {technology.name}.")
                self.hand.cards.append(technology)  # Return the card to hand

    def resolve_technology_effect(self, technology, game_state):
        if technology.spell_effect == "enemy player takes 5 damage":
            game_state.opponent.take_damage(5)
        elif technology.spell_effect == "Owner takes -2 damage from all sources":
            self.shield = -2  # Example implementation
            print(f"{self.name} now takes -2 damage from all sources.")

    def check_dead_creatures(self):
        for card in self.battlefield[:]:
            if card.card_type == "Creature" and card.attributes.get('hp', 0) <= 0:
                print(f"{card.name} has died.")
                self.battlefield.remove(card)
                self.graveyard.append(card)
                # Remove attached equipment and move to graveyard
                for equip in card.attributes.get('equipped', []):
                    print(f"{equip.name} attached to {card.name} has been moved to the graveyard.")
                    self.graveyard.append(equip)
    
    def reset_land_played(self):
        self.land_played = False

    def increase_mana(self):
        if self.mana < self.max_mana:
            self.mana += 1
        print(f"{self.name} now has {self.mana} mana.")

    def use_mana(self, cost: dict) -> bool:
        total_common_cost = cost.get("Common", 0)
        if self.mana >= total_common_cost:
            self.mana -= total_common_cost
            print(f"{self.name} used {total_common_cost} common mana, {self.mana} remaining.")
            return True
        print(f"{self.name} does not have enough common mana. {self.mana} available, {total_common_cost} needed.")
        return False

    def use_resource_mana(self, cost: dict) -> bool:
        for resource_type, amount in cost.items():
            if resource_type != "Common" and self.resource_pool.get(resource_type, 0) < amount:
                print(f"{self.name} does not have enough {resource_type} mana. {self.resource_pool.get(resource_type, 0)} available, {amount} needed.")
                return False
        for resource_type, amount in cost.items():
            if resource_type != "Common":
                self.resource_pool[resource_type] -= amount
        print(f"{self.name} used resource mana: {cost}. Remaining pool: {self.resource_pool}.")
        return True

    def can_pay_cost(self, cost: dict) -> bool:
        common_cost = cost.get("Common", 0)
        if self.mana < common_cost:
            return False
        for resource_type, amount in cost.items():
            if resource_type != "Common" and self.resource_pool.get(resource_type, 0) < amount:
                return False
        return True

    def pay_cost(self, cost: dict):
        self.use_mana({"Common": cost.get("Common", 0)})
        self.use_resource_mana({k: v for k, v in cost.items() if k != "Common"})

    def untap_resource(self, resource_type: str):
        """
        Untap a resource of the given type.
        
        :param resource_type: The type of resource to untap.
        """
        if resource_type in self.resource_pool:
            self.resource_pool[resource_type] += 1
            print(f"{self.name} untapped {resource_type}. Remaining pool: {self.resource_pool}.")
        else:
            print(f"{self.name} does not have {resource_type} to untap.")

    def get_resource_pool(self) -> Dict[str, int]:
        """
        Get the current resource pool of the player.
        
        :return: A dictionary of resource types and their amounts.
        """
        return self.resource_pool

    def draw_initial_hand(self):
        """
        Draw the initial hand of cards from the deck.
        """
        self.hand.draw_initial_hand(self.deck)

    def draw_card(self):
        """
        Draw a card from the deck into the hand.
        """
        self.hand.draw_card(self.deck)

    def display_hand(self):
        """
        Display the current hand of the player.
        """
        self.hand.display()

    def place_card_from_hand(self, card_name: str):
        """
        Place a card from the hand onto the battlefield.
        
        :param card_name: The name of the card to play.
        """
        self.play_card_to_battlefield(card_name)

    def get_battlefield(self) -> List[Card]:
        """
        Get the current cards on the battlefield.
        
        :return: A list of cards on the battlefield.
        """
        return self.battlefield

    def get_hp(self) -> int:
        """
        Get the current HP of the player.
        
        :return: The current HP.
        """
        return self.hp
    
    def get_common_mana(self) -> int:
        """
        Get the current common mana of the player.
        
        :return: The current mana.
        """
        return self.mana

