from Hand import Hand
from Deck import Deck
from Card import Card
from typing import List

class Player:
    def __init__(self, name: str, deck: Deck):
        self.name = name
        self.deck = deck
        self.hand = Hand()
        self.battlefield: List[Card] = []
        self.hp = 40

    def damage(self, damage: int):
        """Reduce player's HP by the given damage amount."""
        self.hp -= damage
        print(f"{self.name} takes {damage} damage and is now at {self.hp} HP.")

    def heal(self, amount: int):
        """Increase player's HP by the given amount."""
        self.hp += amount
        print(f"{self.name} heals {amount} and is now at {self.hp} HP.")

    def play_card_to_battlefield(self, card_name: str):
        """Play a card from hand to the battlefield."""
        card = self.hand.place_card(card_name)
        if card:
            self.battlefield.append(card)
            print(f"{self.name} placed {card} onto the battlefield.")
        else:
            print(f"{self.name} could not find {card_name} in hand to play.")

