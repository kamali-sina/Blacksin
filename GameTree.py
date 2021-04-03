import math

from GameState import GameState


class GameTree:
    def __init__(self, num_of_cards,cpu_cards,player_cards,max_height):
        self.deck_count = num_of_cards
        self.target = self.deck_count * 2 - 1
        # self.cpu_cards = cpu_cards
        # self.player_cards = player_cards
        # self.remained_cards = set(range(1, self.deck_count + 1)) - cpu_cards - player_cards
        self.height = max_height
        self.player_has_stopped = False
        self.nodes = [[] for i in range(self.height+1)]
        self.root = self.make_node(None,0,cpu_cards,player_cards,True,False)
        # self.remained_cards = set(range(1, self.deck_count + 1)) - cpu_cards - player_cards
        # self.has_stopped = False
        # self.__hidden_card = 0

    def make_node(self, action,depth,cpu_cards,player_cards,player_turn,player_stoped):
        node = GameState(self.deck_count ,cpu_cards,player_cards,player_turn, player_stoped,action,depth)
        self.nodes[self.height].append(node)
        return node

    def search_tree(self):
        self.Expectiminimax(self.root,0,True,None)
        decision =  self.root.get_best_decision()
        return decision

    def Expectiminimax(self,node,depth,isRoot,action):
        #stoping the recursive calls condition
        if depth == self.height:
            return node.get_score()
        #<=1 because cpu also has 1 hidden card. this condition is for when the cards are finished.
        if node.get_num_of_remained_cards() <=1:
            return node.get_score()
        if (node.player_has_stopped() and (node.is_player_turn()) and (action == 'S')):
            return node.get_score()

        #creating the tree
        #Draw action creates a chance node
        if action == 'C':
            for card in node.get_remained_cards():
                if node.is_player_turn():
                    new_node = self.make_node('D',depth+1,node.get_cpu_cards(),
                                              node.get_player_cards()| {card},node.is_player_turn(),False)
                    node.set_child(new_node)
                else:
                    new_node = self.make_node('D', depth + 1, node.get_cpu_cards()|{card},
                                              node.get_player_cards(), node.is_player_turn(), False)
                    node.set_child(new_node)
        else:
            stop = self.make_node('S',depth+1,node.get_cpu_cards(),
                                      node.get_player_cards(),not node.is_player_turn(),True)
            node.set_child(stop)
            chance_node = self.make_node('C', depth +1, node.get_cpu_cards(),
                                       node.get_player_cards(), node.is_player_turn(), node.get_player_stopped())
            node.set_child(chance_node)

        #assign values
        if(node.get_action() == 'C'):
            expected_score = 0
            for child in node.get_children():
                expected_score += self.Expectiminimax(child, depth + 1,False,child.get_action())
            return expected_score/node.get_num_of_remained_cards()
        elif(node.is_player_turn()):
            best_value = -math.inf
            for child in node.get_children():
                value = self.Expectiminimax(child, depth + 1,False,child.get_action())
                # best_value = max(value,best_value)
                if (value > best_value):
                    best_value = value
                    node.set_best_decision(child)
            return best_value
        else:
            best_value = math.inf
            for child in node.get_children():
                value = self.Expectiminimax(child, depth + 1,False,child.get_action())
                # best_value = min(best_value,value)
                if (value < best_value):
                    best_value = value
                    node.set_best_decision(child)
            return best_value