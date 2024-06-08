from typing import List, Optional
import random
from Deck import Deck
from Card import Card

class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def shuffle(deck: Deck):
        """Shuffle the deck."""
        random.shuffle(deck.cards)
        print("Deck shuffled.")

    def draw_card(self, deck: Deck) -> Optional[Card]:
        """Draw a card from the top of the deck and add it to the hand."""
        if len(self.cards) >= 8:
            print("Hand is full. Cannot draw more cards.")
            return None
        
        if deck.cards:
            drawn_card = deck.cards.pop(0)
            self.cards.append(drawn_card)
            print(f"Drew {drawn_card} from the deck and added it to the hand.")
            return drawn_card
        
        print("Deck is empty.")
        return None

    def place_card(self, card_name: str) -> Optional[Card]:
        """Place a card down from the hand by name, removing it from the hand."""
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                print(f"Placed {card} from the hand.")
                return card
        
        print(f"Card with name '{card_name}' not found in the hand.")
        return None

    def view_hand(self):
        """View all cards in the hand."""
        if self.cards:
            print("Current hand:")
            for card in self.cards:
                print(f" - {card}")
        else:
            print("The hand is empty.")

    def count(self) -> int:
        """Get the number of cards in the hand."""
        return len(self.cards)

    def draw_initial_hand(self, deck: Deck):
        """
        Draw the initial hand of cards from the deck.

        :param deck: The deck from which to draw the initial hand.
        """
        while len(self.cards) < 8 and deck.cards:
            drawn_card = deck.cards.pop(0)
            self.cards.append(drawn_card)
            print(f"Drew {drawn_card} from the deck and added it to the hand.")
        print("Initial hand drawn.")

    def display(self):
        """Display the current hand of the player."""
        self.view_hand()

    def discard_excess(self, max_hand_size: int, choose_discard: callable):
        """Discard cards until the hand size is reduced to max_hand_size."""
        while len(self.cards) > max_hand_size:
            card_to_discard = choose_discard(self.cards)
            if card_to_discard in self.cards:
                self.cards.remove(card_to_discard)
                print(f"Discarded {card_to_discard} from the hand.")
            else:
                print("Error: chosen card is not in the hand.")
    
    def choose_discard(cards: List[Card]) -> Card:
        """Placeholder function to choose a card to discard."""
        # Simulate player choice - in practice, this would be done through a game UI
        print("Choose a card to discard:")
        for index, card in enumerate(cards):
            print(f"{index + 1}: {card}")
        choice = int(input("Enter the number of the card to discard: ")) - 1
        return cards[choice]
