from Player import Player

class GameState:
    def __init__(self, players):
        self.players = players
        self.active_player_index = 0
        self.phase = "untap"
        self.turn_count = 1
        self.stack = []
        self.fields = {player.name: [] for player in players}
        self.mana_pool = {player.name: 1 for player in players}

    def next_phase(self):
        phases = ["untap", "upkeep", "draw", "main1", "combat", "main2", "end"]
        current_phase_index = phases.index(self.phase)
        self.phase = phases[(current_phase_index + 1) % len(phases)]
        if self.phase == "untap":
            self.next_turn()
        elif self.phase == "draw":
            self.draw_card()

    def next_turn(self):
        self.turn_count += 1
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        active_player = self.get_active_player()
        self.mana_pool[active_player.name] += 1

    def get_active_player(self):
        return self.players[self.active_player_index]

    def draw_card(self):
        player = self.get_active_player()
        player.hand.draw()

    def play_card(self, card):
        player = self.get_active_player()
        if card.mana_cost > self.mana_pool[player.name]:
            print("Not enough mana to play this card.")
            return False
        self.mana_pool[player.name] -= card.mana_cost
        self.fields[player.name].append(card)
        self.apply_card_effects(card)
        return True

    def apply_card_effects(self, card):
        if card.effect:
            card.effect(self)

    def action_phase(self, action_type, card):
        if action_type == "attack":
            self.attack_with_card(card)
        elif action_type == "use_ability":
            self.use_ability(card)

    def attack_with_card(self, attacking_card):
        defender = self.get_defending_player()
        # Assuming defending_card is chosen by some game logic, for example purposes.
        defending_card = None  
        if defending_card and defending_card in self.fields[defender.name]:
            self.resolve_combat(attacking_card, defending_card)
        else:
            print("No defending card available, attacking directly.")

    def resolve_combat(self, attacking_card, defending_card):
        if attacking_card.attack > defending_card.defense:
            self.fields[self.get_defending_player().name].remove(defending_card)
        elif attacking_card.attack < defending_card.defense:
            self.fields[self.get_active_player().name].remove(attacking_card)
        else:
            self.fields[self.get_defending_player().name].remove(defending_card)
            self.fields[self.get_active_player().name].remove(attacking_card)

    def get_defending_player(self):
        return self.players[(self.active_player_index + 1) % len(self.players)]

    def end_turn(self):
        self.phase = "end"
        self.next_phase()
