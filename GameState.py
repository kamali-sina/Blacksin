import math

class GameState:
    def __init__(self,deck_count ,cpu_cards,player_cards,is_player_turn, player_has_stoped,action,depth,remained_erases):
        self.deck_count = deck_count
        self.target = self.deck_count * 2 - 1
        self.cpu_cards = cpu_cards
        self.player_cards = player_cards
        self.remained_cards = list(set(range(1,self.deck_count+1)) - set(cpu_cards) - set(player_cards))
        self.player_turn = is_player_turn
        self.player_has_stoped = player_has_stoped
        self.action = action
        self.remained_erases = remained_erases
        self.depth = depth
        self.children = []
        self.score = None
        self.best_decision = None

    def set_child(self, child_node):
        self.children.append(child_node)

    def eval_score(self):
        player_score = sum(self.player_cards)
        expected_cpu_hidden_card = math.ceil(sum(self.remained_cards)/len(self.remained_cards))
        cpu_score = sum(self.cpu_cards) + expected_cpu_hidden_card
        if self.action == 'C':
            if self.player_turn:
                player_score += expected_cpu_hidden_card
            else:
                cpu_score += expected_cpu_hidden_card

        if player_score > self.target:
            self.score = -10*self.target
        elif cpu_score > self.target:
            self.score = 10*self.target
        else:
            self.score = 9*(player_score - cpu_score) + 1*(self.target - player_score)

    def get_score(self):
        if not self.score:
            self.eval_score()
        return self.score

    def get_num_of_remained_cards(self):
        return len(self.remained_cards)

    def player_has_stopped(self):
        return self.player_has_stoped

    def get_cpu_cards(self):
        return self.cpu_cards

    def get_player_cards(self):
        return self.player_cards

    def get_remained_cards(self):
        return self.remained_cards

    def is_player_turn(self):
        return self.player_turn

    def get_children(self):
        return self.children

    def get_action(self):
        return self.action

    def set_best_decision(self,node):
        self.best_decision = node

    def get_best_decision(self):
        return self.best_decision.get_action()

    def get_player_stopped(self):
        return self.player_has_stoped

    def get_remained_erases(self):
        return self.remained_erases