import math

from GameState import GameState


class GameTree:
    def __init__(self, num_of_cards,cpu_cards,player_cards,max_height,erases_remained):
        self.deck_count = num_of_cards
        self.target = self.deck_count * 2 - 1
        self.height = max_height
        self.player_has_stopped = False
        self.nodes = [[] for i in range(self.height+1)]
        self.root = self.make_node(None,0,cpu_cards,player_cards,True,False,erases_remained)

    def make_node(self, action,depth,cpu_cards,player_cards,player_turn,player_stoped, remained_erases):
        node = GameState(self.deck_count ,cpu_cards,player_cards,player_turn, player_stoped,action,depth,remained_erases)
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
            if isRoot:
                node.set_best_decision(self.make_node('S',depth+1,node.get_cpu_cards(),
                                              node.get_player_cards(),node.is_player_turn(),True,node.get_remained_erases()))
            return node.get_score()
        if (node.player_has_stopped() and (node.is_player_turn()) and (action == 'S')):
            return node.get_score()

        #creating the tree
        #Draw action creates a chance node
        if action == 'C':
            for card in node.get_remained_cards():
                if node.is_player_turn():
                    new_node = self.make_node('D',depth+1,node.get_cpu_cards(),
                                              node.get_player_cards() + [card],not node.is_player_turn(),False,node.get_remained_erases())
                    node.set_child(new_node)
                else:
                    new_node = self.make_node('D', depth + 1, node.get_cpu_cards()+ [card],
                                              node.get_player_cards(), not node.is_player_turn(), False,node.get_remained_erases())
                    node.set_child(new_node)

        else:
            stop = self.make_node('S',depth+1,node.get_cpu_cards(),
                                      node.get_player_cards(),not node.is_player_turn(),True,node.get_remained_erases())
            node.set_child(stop)
            chance_node = self.make_node('C', depth +1, node.get_cpu_cards(),
                                       node.get_player_cards(), node.is_player_turn(), node.get_player_stopped(),node.get_remained_erases())
            node.set_child(chance_node)

            if node.is_player_turn() and not node.player_has_stopped() and node.get_remained_erases() >=1:
                if len(node.get_player_cards())>1:
                    erase_self = self.make_node('es',depth+1,node.get_cpu_cards(),
                                          node.get_player_cards()[:-1],not node.is_player_turn(),False,node.get_remained_erases()-1)
                    node.set_child(erase_self)
                if len(node.get_cpu_cards())>=1:
                    erase_cpu = self.make_node('eo', depth + 1, node.get_cpu_cards()[:-1],
                                               node.get_player_cards(), not node.is_player_turn(), False,
                                                node.get_remained_erases() - 1)
                    node.set_child(erase_cpu)

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
                if (value > best_value ):
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