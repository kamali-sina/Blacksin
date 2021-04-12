import math

class GameState:
    def __init__(self,deck_count ,cpu_cards,player_cards,is_player_turn, player_has_stoped,action,depth,remained_erases, opponent_remaied_erases, deck, cpu_has_stopped):
        self.deck_count = deck_count
        self.target = self.deck_count * 2 - 1
        self.cpu_cards = cpu_cards
        self.player_cards = player_cards
        self.remained_cards = deck
        self.player_turn = is_player_turn
        self.player_has_stopped = player_has_stoped
        self.cpu_has_stopped = cpu_has_stopped
        self.action = action
        self.remained_erases = remained_erases
        self.opponent_remained_erases = opponent_remaied_erases
        self.depth = depth
        self.children = []
        self.score = None
        self.best_decision = None

    def set_child(self, child_node):
        self.children.append(child_node)

    def eval_score(self):
        player_score = sum(self.player_cards)
        # expected_cpu_hidden_card = math.ceil(sum(self.remained_cards)/len(self.remained_cards))
        cpu_score = sum(self.cpu_cards)

        if player_score > self.target:
            self.score = -10*self.target
        elif cpu_score > self.target:
            self.score = 10*self.target
        else:
            self.score = (player_score - cpu_score)
                         # + 1*(self.target - player_score)

    def get_score(self):
        if not self.score:
            self.eval_score()
        return self.score

    def get_num_of_remained_cards(self):
        return len(self.remained_cards)

    def get_children(self):
        return self.children

    def set_best_decision(self,node):
        self.best_decision = node

    def get_best_decision(self):
        return self.best_decision.action

    def player_has_erase_left(self):
        return self.remained_erases >0

    def opponent_has_erase_left(self):
        return self.opponent_remained_erases >0
