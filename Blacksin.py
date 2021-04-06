import random
from time import sleep
from Player import Player

class Blacksin:
    def __init__(self, expert_mode=False, deck_count=11):
        self.deck_count = deck_count
        self.expert_mode = expert_mode
        self.target = self.deck_count * 2 - 1
        self.player = Player('player', deck_count)
        self.cpu = Player('cpu', deck_count)
        self.__deck = self.shuffle_cards()
        self.seen_cards = []
    
    def shuffle_cards(self):
        return list(random.sample(range(1, self.deck_count + 1), self.deck_count))

    def draw_card(self, hidden=False):
        if (len(self.__deck) > 0):
            card = self.__deck.pop(0)
            if (not hidden):
                self.seen_cards.append(card)
            return card
        print('The deck is empty! ending game...')
        self.cpu.has_stopped = True
        self.player.has_stopped = True
        return -1

    def handout_cards(self):
        self.player.draw_card(self.draw_card())
        self.cpu.draw_card(self.draw_card())
        self.player.set_hidden_card(self.draw_card(hidden=True))
        self.cpu.set_hidden_card(self.draw_card(hidden=True))
    
    def handle_input(self, _input, player):
        if (player is self.player):
            opponent = self.cpu
        else:
            opponent = self.player
        if (_input == 'stop' or _input == 's'):
            player.has_stopped = True
            print(f'{player.name} has stopped')
        elif (_input == 'draw' or _input == 'd'):
            card = self.draw_card()
            if (card == -1): return True
            player.draw_card(card)
            print(f'{player.name} drawed a card: {card}')
            if (self.expert_mode):
                opponent.has_stopped = False
        elif ((_input == 'erase_self' or _input == 'es') and self.expert_mode):
            player.erase(player)
            if (self.expert_mode):
                opponent.has_stopped = False
        elif ((_input == 'erase_opponent' or _input == 'eo') and self.expert_mode):
            player.erase(opponent)
            if (self.expert_mode):
                opponent.has_stopped = False
        else:
            print('ERROR: unknown command')
            return False
        return True

    def get_player_input(self):
        result = False
        while(not result):
            player_input = input('>').strip().lower()
            result = self.handle_input(player_input, self.player)
            
    def cpu_play(self):
        try:
            cpu_input = self.cpu.play(self.seen_cards, self.expert_mode)
        except:
            cpu_input = 'stop'
        self.handle_input(cpu_input, self.cpu)

    def check_for_winners(self):
        self.cpu.print_info()
        self.player.print_info()
        player_margin = self.player.finish()
        cpu_margin = self.cpu.finish()
        player_win_condition_1 = cpu_margin < 0 and player_margin >= 0
        player_win_condition_2 = cpu_margin >=0 and player_margin >= 0 and player_margin < cpu_margin
        draw_condition_1 = cpu_margin < 0 and player_margin < 0
        draw_condition_2 = cpu_margin >= 0 and player_margin >= 0 and player_margin == cpu_margin
        cpu_win_condition_1 = player_margin < 0 and cpu_margin >= 0
        cpu_win_condition_2 = cpu_margin >=0 and player_margin >= 0 and player_margin > cpu_margin
        if (player_win_condition_1 or player_win_condition_2):
            print('the winner is the player!')
            return 1
        elif(draw_condition_1 or draw_condition_2):
            print('the game ends in a draw!')
            return 0
        elif(cpu_win_condition_1 or cpu_win_condition_2):
            print('the winner is the cpu!')
            return -1
        else:
            print('an error has accurred! exiting...')
            exit()

    def run(self):
        print('\nstarting game... shuffling... handing out cards...')
        print(f'remember, you are aiming for nearest to: {self.deck_count * 2 - 1}')
        self.handout_cards()
        turn = 0
        while(not self.player.has_stopped or not self.cpu.has_stopped):
            if (turn == 0):
                if (not self.player.has_stopped):
                    self.cpu.print_info(hidden=True)
                    self.player.print_info()
                    self.get_player_input()
                    print()
            else:
                if (not self.cpu.has_stopped):
                    print('cpu playing...')
                    sleep(1)
                    self.cpu_play()
                    print()
            turn = 1 - turn
        print('\nand the winner is...')
        sleep(1)
        return self.check_for_winners()

if (__name__ == '__main__'):
    s = Blacksin(expert_mode=False, deck_count=7)
    s.run()