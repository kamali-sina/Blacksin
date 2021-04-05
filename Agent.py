from GameTree import GameTree
import random

def move(num_of_cards,cpu_cards,player_cards, tree_height):
    gameTree = GameTree(num_of_cards,cpu_cards,player_cards,tree_height)
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