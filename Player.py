class Player:
    def __init__(self, name, num_of_cards):
        self.name = name
        self.deck_count = num_of_cards
        self.target = self.deck_count * 2 - 1
        self.cards = []
        self.erases_remaining = self.deck_count // 5
        self.has_stopped = False

    def draw_card(self, card):
        self.cards.append(card)

    def print_info(self):
        print(f"{self.name}'s cards: ", end='')
        for c in self.cards:
            print(f'{c}, ', end='')
        print(f'sum: {sum(self.cards)}')
    
    def finish(self):
        return self.target - sum(self.cards)
    
    def calculate_mean(self, seen_cards):
        sum_of_seen_cards = sum(seen_cards)
        num_of_seen_cards = len(seen_cards) + 1
        sum_of_remaining_cards = ((self.deck_count * (self.deck_count + 1))/2) - sum_of_seen_cards
        mean_of_remaining_cards = sum_of_remaining_cards / (self.deck_count - num_of_seen_cards)
        return mean_of_remaining_cards
    
    def play(self, seen_cards, expert_mode, deck, enemies_cards):
        if (len(deck) > 0):
            next_card_in_deck = deck[0]
        else:
            next_card_in_deck = 0
        if (len(deck) > 1):
            next_enemy_card_in_deck = deck[1]
        else:
            next_enemy_card_in_deck = 0
        amount_to_target = self.target - sum(self.cards)
        amount_with_next_card = self.target - (sum(self.cards) + next_card_in_deck)
        enemies_amount_to_target = self.target - sum(enemies_cards)
        enemies_amount_with_next_card = self.target - (sum(enemies_cards) + next_enemy_card_in_deck)
        print(next_card_in_deck)
        _stop_condition = amount_to_target < next_card_in_deck and self.erases_remaining <= 0
        _draw_condition_1 = next_card_in_deck != 0
        _draw_condition_2 = amount_with_next_card >= 0
        print(amount_with_next_card)
        _erase_condition = self.erases_remaining > 0 and expert_mode
        _erase_self_condition = amount_to_target < 0
        _erase_opponent_condition_or = enemies_amount_to_target < (self.target //7)
        _erase_opponent_condition_or_2 = enemies_amount_with_next_card < (self.target // 7) 
        _erase_opponent_condition_or_3 = enemies_amount_with_next_card <= amount_with_next_card
        _erase_opponent_condition_or_4 = enemies_amount_to_target <= amount_to_target
        _erase_opponent_condition = _erase_opponent_condition_or or _erase_opponent_condition_or_2 or _erase_opponent_condition_or_3
        _erase_opponent_condition = _erase_opponent_condition or _erase_opponent_condition_or_4 
        if (_stop_condition): 
            print('stop 1')
            return 'stop'
        elif (_draw_condition_1 and _draw_condition_2):
            return 'draw'
        elif(_erase_self_condition and _erase_condition):
            return 'erase_self'
        elif(_erase_opponent_condition and _erase_condition):
            return 'erase_opponent'
        else:
            print('stop 2')
            return 'stop'
    
    def erase(self, target):
        if (len(target.cards) == 0):
            print(f'{target.name} has no more eraseble cards!')
            return
        if (self.erases_remaining > 0):
            self.erases_remaining -= 1
            card = target.cards.pop(-1)
            print(f'{self.name} erased {card} from {target.name}\'s deck!')
            return
        print(f'{self.name} has no more erases remaining!')

    def get_player_cards(self):
        return self.cards

    def get_erases_remained(self):
        return self.erases_remaining