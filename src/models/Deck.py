import random
from Card import Card 
from typing import List, Optional

class Deck:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        """Add a card to the deck, ensuring the deck does not exceed 60 cards."""
        if len(self.cards) < 60:
            self.cards.append(card)
            # print(f"Added {card} to the deck.")
        else:
            print("Cannot add more cards. The deck is already at its maximum capacity of 60 cards.")

    def remove_card(self, card_name: str) -> Optional[Card]:
        """Remove a card from the deck by name, ensuring the deck is not empty."""
        if not self.cards:
            print("The deck is empty. No cards to remove.")
            return None
        
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                # print(f"Removed {card} from the deck.")
                return card
        
        print(f"Card with name '{card_name}' not found in the deck.")
        return None
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        print("Deck shuffled.")

    def view_deck(self):
        """View all cards in the deck."""
        if self.cards:
            print("Current deck:")
            for card in self.cards:
                print(f" - {card}")
        else:
            print("The deck is empty.")

    def count(self) -> int:
        """Get the number of cards in the deck."""
        return len(self.cards)

# Example usage:
if __name__ == "__main__":
    # Create some example cards
    card1 = Card(name="Fire Elemental", card_type="Creature", attributes={"attack": 5, "defense": 4})
    card2 = Card(name="Healing Potion", card_type="Spell", attributes={"heal": 10})
    card3 = Card(name="Lightning Bolt", card_type="Spell", attributes={"damage": 7})

    # Create a deck and add cards to it
    deck = Deck()
    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)

    # View deck
    deck.view_deck()

    # Shuffle the deck
    # deck.shuffle()

    # Draw a card
    # deck.draw_card()

    # Remove a card by name
    deck.remove_card("Healing Potion")

    # View deck again
    deck.view_deck()

    # Count cards in the deck
    print(f"Number of cards in the deck: {deck.count()}")