from Hand import Hand

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = Hand(deck)
