import copy
import math

from GameState import GameState


class GameTree:
    def __init__(self, num_of_cards,cpu_cards,player_cards,max_height,erases_remained,opponent_erases_remained, deck, cpu_has_stopped):
        self.deck_count = num_of_cards
        self.target = self.deck_count * 2 - 1
        self.height = max_height
        self.player_has_stopped = False
        self.nodes = [[] for i in range(self.height+1)]
        self.root = self.make_node(None,0,cpu_cards,player_cards,True,False,erases_remained,opponent_erases_remained, deck, cpu_has_stopped)

    def make_node(self, action,depth,cpu_cards,player_cards,player_turn,player_stoped, remained_erases, opponent_erases_remained, deck, cpu_has_stopped):
        node = GameState(self.deck_count ,cpu_cards,copy.deepcopy(player_cards),player_turn, player_stoped,action,depth,remained_erases,opponent_erases_remained, deck, cpu_has_stopped)
        self.nodes[depth].append(node)
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
        if node.get_num_of_remained_cards() <=0:
            if isRoot:
                node.set_best_decision(self.make_node('S',depth+1,node.get_cpu_cards(),
                                              node.get_player_cards(),node.is_player_turn(),True,node.get_remained_erases(),
                                              node.get_opponent_remained_erases(),node.get_remained_cards(),node.cpu_has_stopped))
            return node.get_score()
        if (node.player_has_stopped() and node.cpu_has_stopped):
            return node.get_score()

        #creating the tree
        stop = self.make_node('s',depth+1,node.get_cpu_cards(),
                                  node.get_player_cards(),not node.is_player_turn(),True,node.get_remained_erases(),node.get_opponent_remained_erases(),node.get_remained_cards(),node.cpu_has_stopped)
        node.set_child(stop)
        new_card = node.get_remained_cards()[0]
        new_deck = node.get_remained_cards()[1:]
        if node.is_player_turn():
            draw_node = self.make_node('d', depth +1, node.get_cpu_cards(),
                                   node.get_player_cards().append(new_card), not node.is_player_turn(), node.get_player_stopped(),
                                       node.get_remained_erases(),node.get_opponent_remained_erases(),new_deck, node.cpu_has_stopped)
        else:
            draw_node = self.make_node('d', depth +1, node.get_cpu_cards().append(new_card),
                                   node.get_player_cards(), not node.is_player_turn(), node.get_player_stopped(),
                                       node.get_remained_erases(),node.get_opponent_remained_erases(),new_deck, node.cpu_has_stopped)
        node.set_child(draw_node)

        if node.is_player_turn() and not node.player_has_stopped() and node.player_has_erase_left():
            if len(node.get_player_cards())>1:
                erase_self = self.make_node('es',depth+1,node.get_cpu_cards(),
                                      node.get_player_cards()[:-1] ,not node.is_player_turn(),
                                            False,node.get_remained_erases()-1,node.get_opponent_remained_erases(),node.get_remained_cards(), node.cpu_has_stopped)
                node.set_child(erase_self)
            if len(node.get_cpu_cards())>1:
                erase_cpu = self.make_node('eo', depth + 1, node.get_cpu_cards()[:-1],
                                           node.get_player_cards(), not node.is_player_turn(), False,
                                            node.get_remained_erases() - 1,node.get_opponent_remained_erases(),node.get_remained_cards(), node.cpu_has_stopped)
                node.set_child(erase_cpu)
        if not node.is_player_turn() and not node.cpu_has_stopped and node.opponent_has_erase_left():
            if len(node.get_player_cards())>1:
                erase_opponent = self.make_node('eo',depth+1,node.get_cpu_cards(),
                                      node.get_player_cards()[:-1] ,not node.is_player_turn(),
                                            False,node.get_remained_erases(),node.get_opponent_remained_erases()-1,node.get_remained_cards(), node.cpu_has_stopped)
                node.set_child(erase_opponent)
            if len(node.get_cpu_cards())>1:
                erase_cpu = self.make_node('es', depth + 1, node.get_cpu_cards()[:-1],
                                           node.get_player_cards(), not node.is_player_turn(), False,
                                            node.get_remained_erases() ,node.get_opponent_remained_erases()-1,node.get_remained_cards(), node.cpu_has_stopped)
                node.set_child(erase_cpu)

        #assign values
        if(node.is_player_turn()):
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