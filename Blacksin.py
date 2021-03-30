import random

class Player:
    def __init__(self):
        self.cards = []
        self.__hidden_card = 0

    def draw_card(self, card):
        self.cards.append(card)
    
    def set_hidden_card(self, card):
        self.__hidden_card = card

    def print_info(self):
        print('you have: ', end='')
        for c in self.cards:
            print(f'c, ', end='')
        print(f'and the hidden card: {self.__hidden_card}')
    

class Blacksin:
    def __init__(self, deck_count=11):
        self.deck_count = deck_count
        self.target = self.deck_count * 2 - 1
        self.player = Player()
        self.cpu = Player()
        self.has_player_stopped = False
        self.has_cpu_stopped = False
        self.__deck = self.shuffle_cards()
    
    def shuffle_cards(self):
        return list(random.sample(range(1, self.deck_count + 1), self.deck_count))

    def draw_card(self):
        return self.__deck.pop(0)

    def handout_cards(self):
        self.player.draw_card(self.draw_card())
        self.cpu.draw_card(self.draw_card())
        self.player.set_hidden_card(self.draw_card())
        self.cpu.set_hidden_card(self.draw_card())

    def get_player_input(self):
        while(1):
            player_input = input('>')
            if (player_input == 'stop' or player_input == 's'):
                self.has_player_stopped = True
                print('you have stopped ')
            elif (player_input == 'draw' or player_input == 'd'):
                self.player_cards.append(self.draw_card())
                print(f'player drawed a card: [{self.player_cards[-1]}]')
            else:
                print('ERROR: unknown command')
                continue
            return
            
    def cpu_play(self):
        amount_left = self.target - sum(self.cpu_cards)
        #calculate mean of remaining cards

    def run(self):
        print('\nstarting game... shuffling... handing out cards...')
        print(f'remember, you are aiming for nearest to: {self.deck_count * 2 - 1}')
        self.handout_cards()
        print(f'you have: {self.player.cards[0]} and [{self.player.}]')
        print(f'cpu has : {self.cpu_cards[0]} and [unknown]')
        turn = 0
        while(1):
            if (turn == 0):
                if (not self.has_player_stopped):
                    self.get_player_input()
            else:
                if (not self.has_cpu_stopped):
                    self.cpu_play()
            turn = 1 - turn

s = Blacksin()
s.run()