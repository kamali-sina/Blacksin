from GameTree import GameTree


def move(num_of_cards,cpu_cards,player_cards):
    gameTree = GameTree(num_of_cards,cpu_cards,player_cards,4)
    result= gameTree.search_tree()
    if(result == 'C'):
        return 'D'
    return result