from Blacksin import Blacksin
import csv

def test():
    for deck_count in [7,11,21,31,41]:
        for tree_height in range(1,4):
            draws = 0
            agent_wins = 0
            for i in range(500):
                s = Blacksin(True,deck_count,tree_height)
                result = s.run()
                if(result == 0):
                    draws+=1
                elif(result == 1):
                    agent_wins+=1
            agent_wins = agent_wins/500
            draws = draws/500
            fields = [deck_count,tree_height,draws,agent_wins,1]
            with open("without_pruning.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            f.close()

if (__name__ == '__main__'):
    test()