# A dictionary to store user stats. In a real application, use a database.
user_stats = {}

from Card import Card

class User:
    def __init__(self, discord_id, victories=0, losses=0, most_played_card=None):
        self.discord_id = discord_id
        self.victories = victories
        self.losses = losses
        self.most_played_card = most_played_card

    def to_dict(self):
        return {
            "discord_id": self.discord_id,
            "victories": self.victories,
            "losses": self.losses,
            "most_played_card": self.most_played_card.to_dict() if self.most_played_card else None
        }

    @classmethod
    def from_dict(cls, data):
        most_played_card = Card.from_dict(data["most_played_card"]) if data["most_played_card"] else None
        return cls(
            discord_id=data["discord_id"],
            victories=data["victories"],
            losses=data["losses"],
            most_played_card=most_played_card
        )
