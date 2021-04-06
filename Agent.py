from GameTree import GameTree
import random

def move(num_of_cards,cpu_cards,player_cards, tree_height,erases_remained):
    gameTree = GameTree(num_of_cards,cpu_cards,player_cards,tree_height,erases_remained)
    result= gameTree.search_tree()
    if(result == 'C'):
        return 'D'
    return result

# def move(num_of_cards,cpu_cards,player_cards, tree_height):
#     r = random.uniform(0, 1)
#     if(r == 0):
#         return 'D'
#     else:
#         return 'S'


if (__name__ == '__main__'):
    move(11,[7,2,6],[4,11],3)