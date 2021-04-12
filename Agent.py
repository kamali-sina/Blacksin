from GameTree import GameTree
import random

def move(player,cpu,deck, tree_height):
    gameTree = GameTree(player,cpu,deck,tree_height)
    result= gameTree.search_tree()
    return result

# def move(num_of_cards,cpu_cards,player_cards, tree_height, erases_remained):
#     r = random.randint(0, 4)
#     if(r == 0):
#         return 'D'
#     elif(r== 1):
#         return 'S'
#     elif (r == 2):
#         return 'es'
#     else:
#         return 'eo'



if (__name__ == '__main__'):
    move(11,[7,2,6],[4,11],3)