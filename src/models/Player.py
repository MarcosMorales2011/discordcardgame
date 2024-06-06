from Hand import Hand
from Deck import Deck
from typing import List
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
            if card.card_type == "Land" and self.land_played:
                print(f"{self.name} cannot play another land this turn.")
            else:
                if card.card_type == "Land":
                    self.land_played = True
                self.battlefield.append(card)
                if card.card_type == "Resource":
                    for resource_type, amount in card.attributes.items():
                        self.resource_pool[resource_type] += amount
                print(f"{self.name} placed {card} onto the battlefield.")
        else:
            print(f"{self.name} could not find {card_name} in hand to play.")

    def reset_land_played(self):
        self.land_played = False

    def increase_mana(self):
        if self.mana < self.max_mana:
            self.mana += 1
        print(f"{self.name} now has {self.mana} mana.")

    def use_mana(self, cost: int) -> bool:
        if self.mana >= cost:
            self.mana -= cost
            print(f"{self.name} used {cost} mana, {self.mana} remaining.")
            return True
        print(f"{self.name} does not have enough mana. {self.mana} available, {cost} needed.")
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
