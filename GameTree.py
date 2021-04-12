import copy
import math

from GameState import GameState


class GameTree:
    def __init__(self, player,cpu, deck, tree_height):
        self.height = tree_height
        self.nodes = [[] for i in range(self.height+1)]
        self.deck_count = player.deck_count
        self.root = self.make_node(None,0,cpu.cards,player.cards,True,False,player.erases_remaining,cpu.erases_remaining, deck, cpu.has_stopped)

    def make_node(self, action,depth,cpu_cards,player_cards,player_turn,player_stoped, remained_erases, opponent_erases_remained, deck, cpu_has_stopped):
        node = GameState(self.deck_count ,cpu_cards,player_cards,player_turn, player_stoped,action,depth,remained_erases,opponent_erases_remained, deck, cpu_has_stopped)
        self.nodes[depth].append(node)
        return node

    def search_tree(self):
        self.alphabeta(self.root,0,True,-math.inf,math.inf)
        decision =  self.root.get_best_decision()
        return decision

    def alphabeta(self,node,depth,isRoot,alpha,beta):
        #stoping the recursive calls condition
        if depth == self.height:
            return node.get_score()
        #<=1 because cpu also has 1 hidden card. this condition is for when the cards are finished.
        if node.get_num_of_remained_cards() <=0:
            if isRoot:
                node.set_best_decision(self.make_node('s',depth+1,node.cpu_cards,
                                              node.player_cards,not node.player_turn,True,node.remained_erases,
                                              node.opponent_remained_erases,node.remained_cards,node.cpu_has_stopped))
            return node.get_score()
        if (node.player_has_stopped and node.cpu_has_stopped):
            return node.get_score()

        #creating the tree
        if node.player_turn:
            stop = self.make_node('s', depth + 1, node.cpu_cards,
                                  node.player_cards, not node.player_turn, True, node.remained_erases,
                                  node.opponent_remained_erases, node.remained_cards, node.cpu_has_stopped)
            node.set_child(stop)
            new_card = [node.remained_cards[0]]
            new_deck = node.remained_cards[1:]
            draw_node = self.make_node('d', depth + 1, node.cpu_cards,
                                       node.player_cards + new_card, not node.player_turn, node.player_has_stopped,
                                       node.remained_erases, node.opponent_remained_erases, new_deck,
                                       node.cpu_has_stopped)
            node.set_child(draw_node)
            if not node.player_has_stopped and node.player_has_erase_left():
                if len(node.player_cards) > 1:
                    erase_self = self.make_node('es', depth + 1, node.cpu_cards,
                                                node.player_cards[:-1], not node.player_turn,
                                                False, node.remained_erases - 1, node.opponent_remained_erases,
                                                node.remained_cards, node.cpu_has_stopped)
                    node.set_child(erase_self)
                if len(node.cpu_cards) > 1:
                    erase_cpu = self.make_node('eo', depth + 1, node.cpu_cards[:-1],
                                               node.player_cards, not node.player_turn, False,
                                               node.remained_erases - 1, node.opponent_remained_erases,
                                               node.remained_cards, node.cpu_has_stopped)
                    node.set_child(erase_cpu)


        else:
            stop = self.make_node('s',depth+1,node.cpu_cards,
                                  node.player_cards,not node.player_turn,node.player_has_stopped,node.remained_erases,node.opponent_remained_erases,node.remained_cards,True)
            node.set_child(stop)

            new_card = [node.remained_cards[0]]
            new_deck = node.remained_cards[1:]
            draw_node = self.make_node('d', depth +1, node.cpu_cards +new_card,
                                   node.player_cards, not node.player_turn, node.player_has_stopped,
                                       node.remained_erases,node.opponent_remained_erases,new_deck, node.cpu_has_stopped)
            node.set_child(draw_node)
            if not node.cpu_has_stopped and node.opponent_has_erase_left():
                if len(node.player_cards)>1:
                    erase_opponent = self.make_node('eo',depth+1,node.cpu_cards,
                                          node.player_cards[:-1] ,not node.player_turn,
                                                node.player_has_stopped,node.remained_erases,node.opponent_remained_erases-1,node.remained_cards, node.cpu_has_stopped)
                    node.set_child(erase_opponent)
                if len(node.cpu_cards)>1:
                    erase_cpu = self.make_node('es', depth + 1, node.cpu_cards[:-1],
                                               node.player_cards, not node.player_turn, node.player_has_stopped,
                                                node.remained_erases ,node.opponent_remained_erases-1,node.remained_cards, node.cpu_has_stopped)
                    node.set_child(erase_cpu)

        #assign values
        if(node.player_turn):
            best_value = -math.inf
            for child in node.get_children():
                value = self.alphabeta(child, depth + 1,False,alpha,beta)
                # best_value = max(value,best_value)
                if (value > best_value ):
                    best_value = value
                    node.set_best_decision(child)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = math.inf
            for child in node.get_children():
                value = self.alphabeta(child, depth + 1,False,alpha,beta)
                # best_value = min(best_value,value)
                if (value < best_value):
                    best_value = value
                    node.set_best_decision(child)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value