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
        self.mana_pool = 0

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
                print(f"{self.name} placed {card} onto the battlefield.")
        else:
            print(f"{self.name} could not find {card_name} in hand to play.")

    def reset_land_played(self):
        self.land_played = False

    def increase_mana(self):
        if self.mana < 10:
            self.mana += 1
        self.mana_pool = self.mana
        print(f"{self.name} now has {self.mana} mana.")

    def use_mana(self, amount: int) -> bool:
        if self.mana_pool >= amount:
            self.mana_pool -= amount
            print(f"{self.name} used {amount} mana, {self.mana_pool} remaining.")
            return True
        print(f"{self.name} does not have enough mana. {self.mana_pool} available, {amount} needed.")
        return False
