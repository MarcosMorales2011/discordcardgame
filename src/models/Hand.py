import random
from Deck import deck
class Hand:
    def shuffle(deck):
            """Shuffle the deck."""
            random.shuffle(deck.cards)
            print("Deck shuffled.")

    def draw_card(deck) -> Optional[Card]:
        """Draw a card from the top of the deck."""
        if deck.cards:
            drawn_card = deck.cards.pop(0)
            print(f"Drew {drawn_card} from the deck.")
            return drawn_card
        print("Deck is empty.")
        return None