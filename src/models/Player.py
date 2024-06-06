from Hand import Hand
from Deck import Deck
from typing import List, Dict
from Card import Card

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
        self.resource_pool = {"Biology": 0, "Chemistry": 0, "Physics": 0, "Robotics": 0}

    def take_damage(self, damage: int):
        self.hp -= damage
        print(f"{self.name} takes {damage} damage and is now at {self.hp} HP.")

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

    def reset_land_played(self):
        self.land_played = False

    def increase_mana(self):
        if self.mana < self.max_mana:
            self.mana += 1
        print(f"{self.name} now has {self.mana} mana.")

    def use_mana(self, cost: dict) -> bool:
        total_cost = sum(cost.values())
        if self.mana >= total_cost:
            if "Common" in cost:
                self.mana -= total_cost
            print(f"{self.name} used {total_cost} mana, {self.mana} remaining.")
            return True
        print(f"{self.name} does not have enough mana. {self.mana} available, {total_cost} needed.")
        return False

    def use_resource_mana(self, cost: dict) -> bool:
        for resource_type, amount in cost.items():
            if self.resource_pool[resource_type] < amount:
                print(f"{self.name} does not have enough {resource_type} mana. {self.resource_pool[resource_type]} available, {amount} needed.")
                return False
        for resource_type, amount in cost.items():
            self.resource_pool[resource_type] -= amount
        print(f"{self.name} used resource mana: {cost}. Remaining pool: {self.resource_pool}.")
        return True

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
