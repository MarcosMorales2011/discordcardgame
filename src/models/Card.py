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
    
    def get_cost(self, mana_type: str):
        """
        Get the value of a specific attribute.
        
        :param mana_type: The name of the mana type to retrieve.
        :return: The value of the attribute if it exists, otherwise None.
        """
        return self.attributes.get(mana_type, None)
    
    def tap(self):
        self.tapped = True

    def untap(self):
        self.tapped = False

class Creature(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, hp: int, abilities: list = None):
        super().__init__(name, "Creature", attributes, cost)
        self.hp = hp
        self.abilities = abilities if abilities else []

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        abilities_str = ', '.join(self.abilities)
        return f"Creature: {self.name}\nHP: {self.hp}\nAttributes: {attributes_str}\nCost: {self.cost}\nAbilities: {abilities_str}"

    def take_damage(self, damage: int):
        """
        Apply damage to the creature.

        :param damage: The amount of damage to apply.
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

class Resource(Card):
    def __init__(self, name: str, resource_type: str, amount: int, cost: dict):
        attributes = {resource_type: amount}
        super().__init__(name, "Resource", attributes, cost)
        self.resource_type = resource_type
        self.amount = amount

    def __str__(self):
        return f"Resource: {self.name}\nType: {self.resource_type}\nAmount: {self.amount}\nCost: {self.cost}"

class Trap(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, trigger_condition: str, triggered: bool):
        super().__init__(name, "Trap", attributes, cost)
        self.trigger_condition = trigger_condition
        self.triggered = triggered

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        return f"Trap: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nTrigger: {self.trigger_condition}"
    
    def trigger(self):
        """
        Trigger the trap.
        """
        self.triggered = True

class Equipment(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, effects: dict):
        super().__init__(name, "Equipment", attributes, cost)
        self.effects = effects

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        effects_str = ', '.join([f"{key}: {value}" for key, value in self.effects.items()])
        return f"Equipment: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nEffects: {effects_str}"


class Technologies(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, spell_effect: str):
        super().__init__(name, "Technologies", attributes, cost)
        self.spell_effect = spell_effect

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        return f"Technologies: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nEffect: {self.spell_effect}" 