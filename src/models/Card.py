class Card:
    def __init__(self, name: str, card_type: str, attributes: dict, cost: dict, upkeep_cost: dict = None, upkeep_ability: callable = None):
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
        self.upkeep_cost = upkeep_cost or {}
        self.upkeep_ability = upkeep_ability
        self.single_use = attributes.get('single_use', False)

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
    def __init__(self, name: str, attributes: dict, cost: dict, trigger_condition: str, effect: callable):
        super().__init__(name, "Trap", attributes, cost, is_trap=True, trigger_condition=trigger_condition, effect=effect)
        self.triggered = False

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        return f"Trap: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nTrigger Condition: {self.trigger_condition}"

    def trigger(self, game_state, target):
        """
        Trigger the trap's effect.
        """
        if not self.triggered:
            self.triggered = True
            self.effect(game_state, target)
            print(f"Trap {self.name} triggered!")

class Equipment(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, attachment_cost: dict, effects: dict):
        super().__init__(name, "Equipment", attributes, cost)
        self.attachment_cost = attachment_cost
        self.effects = effects
        self.attached_to = None

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        effects_str = ', '.join([f"{key}: {value}" for key, value in self.effects.items()])
        return f"Equipment: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nAttachment Cost: {self.attachment_cost}\nEffects: {effects_str}"

    def attach_to(self, target_creature):
        """
        Attach this equipment to a target creature.
        """
        if target_creature:
            self.attached_to = target_creature
            target_creature.equipment.append(self)
            for effect, value in self.effects.items():
                if effect == "damage":
                    target_creature.attributes["damage"] += value
                elif effect == "revival":
                    target_creature.attributes["alive"] = True
                ## More Elifs to be added in the future.
            print(f"{self.name} has been attached to {target_creature.name}.")



class Technologies(Card):
    def __init__(self, name: str, attributes: dict, cost: dict, spell_effect: dict):
        super().__init__(name, "Technologies", attributes, cost)
        self.spell_effect = spell_effect

    def __str__(self):
        attributes_str = ', '.join([f"{key}: {value}" for key, value in self.attributes.items()])
        effects_str = ', '.join([f"{key}: {value}" for key, value in self.spell_effect.items()])
        return f"Technologies: {self.name}\nAttributes: {attributes_str}\nCost: {self.cost}\nEffect: {effects_str}"

    def activate(self, game_state):
        """Activate the technology's effect."""
        for effect, value in self.spell_effect.items():
            if effect == "damage_enemy":
                game_state.opponent.hp -= value
                print(f"{game_state.opponent.name} takes {value} damage.")
            elif effect == "reduce_damage":
                game_state.current_player.damage_reduction += value
                print(f"{game_state.current_player.name} takes -{value} damage from all sources.")
