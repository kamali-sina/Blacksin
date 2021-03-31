class Player:
    def __init__(self, name, num_of_cards):
        self.name = name
        self.deck_count = num_of_cards
        self.target = self.deck_count * 2 - 1
        self.cards = []
        self.has_stopped = False
        self.__hidden_card = 0

    def draw_card(self, card):
        self.cards.append(card)
    
    def set_hidden_card(self, card):
        self.__hidden_card = card

    def print_info(self, hidden=False):
        print(f"{self.name}'s cards: ", end='')
        for c in self.cards:
            print(f'{c}, ', end='')
        if (hidden):
            print(f'[hidden] sum: {sum(self.cards)} + ?')
        else:
            print(f'[{self.__hidden_card}] sum: {sum(self.cards) + self.__hidden_card}')
    
    def finish(self):
        return self.target - sum(self.cards) - self.__hidden_card
    
    def calculate_mean(self, seen_cards):
        sum_of_seen_cards = sum(seen_cards) + self.__hidden_card
        num_of_seen_cards = len(seen_cards) + 1
        sum_of_remaining_cards = ((self.deck_count * (self.deck_count + 1))/2) - sum_of_seen_cards
        mean_of_remaining_cards = sum_of_remaining_cards / (self.deck_count - num_of_seen_cards)
        return mean_of_remaining_cards
    
    def play(self, seen_cards):
        amount_to_target = self.target - sum(self.cards) - self.__hidden_card
        mean_of_remaining_cards = self.calculate_mean(seen_cards)
        if (amount_to_target >= mean_of_remaining_cards - 1):
            return 'draw'
        else:
            return 'stop'