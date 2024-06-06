class Card:
    def __init__(self, name: str, card_type: str, attributes: dict, cost: dict):
        """
        Initialize a card with a name, card type, and attributes.
        
        :param name: The name of the card.
        :param card_type: The type of the card (e.g., "Creature", "Spell").
        :param attributes: A dictionary of card attributes (e.g., {"attack": 5, "defense": 4}).
        """
        self.name = name
        self.card_type = card_type
        self.attributes = attributes
        self.cost = cost
        self.tapped = False

    def __repr__(self):
        """
        Provide a string representation of the card for easier debugging.
        
        :return: A string representation of the card.
        """
        return f"{self.name} ({self.card_type})"

    def __str__(self):
        """
        Provide a user-friendly string representation of the card.
        
        :return: A detailed string representation of the card.
        """
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        return f"Card: {self.name}\nType: {self.card_type}\nAttributes: {attributes_str}"

    def get_attribute(self, attribute_name: str):
        """
        Get the value of a specific attribute.
        
        :param attribute_name: The name of the attribute to retrieve.
        :return: The value of the attribute if it exists, otherwise None.
        """
        return self.attributes.get(attribute_name, None)
    
    def get_cost(self, mana_type: str):
        """
        Get the value of a specific attribute.
        
        :param mana_type: The name of the mana type to retrieve.
        :return: The value of the attribute if it exists, otherwise None.
        """
        return self.attributes.get(mana_type, None)
            
    def set_attribute(self, attribute_name: str, value):
        """
        Set the value of a specific attribute.
        
        :param attribute_name: The name of the attribute to set.
        :param value: The value to set for the attribute.
        """
        self.attributes[attribute_name] = value

    def has_attribute(self, attribute_name: str) -> bool:
        """
        Check if the card has a specific attribute.
        
        :param attribute_name: The name of the attribute to check.
        :return: True if the attribute exists, otherwise False.
        """
        return attribute_name in self.attributes
    
    def tap(self):
        self.tapped = True

    def untap(self):
        self.tapped = False

# Example usage:
if __name__ == "__main__":
    # Create a card with attributes
    card = Card(name="Fire Elemental", card_type="Creature", attributes={"attack": 5, "defense": 4, "element": "fire"})

    # Print the card
    print(card)

    # Get an attribute
    attack_value = card.get_attribute("attack")
    print(f"Attack value: {attack_value}")

    # Set an attribute
    card.set_attribute("attack", 6)
    print(f"Updated attack value: {card.get_attribute('attack')}")

    # Check if an attribute exists
    has_element = card.has_attribute("element")
    print(f"Has element attribute: {has_element}")

    # Print the detailed string representation
    print(str(card))

class Creature(Card):
    print("Temp")
    
class Resource(Card):
    print("Temp")

class Trap(Card):
    print("Temp")

class Equipment(Card):
    print("Temp")

class Technologies(Card):
    print("Temp")