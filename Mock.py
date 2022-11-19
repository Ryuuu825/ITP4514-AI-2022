import Engine
from Data import * 

import random



Engine = Engine.Engine()

def main():
    for i in range(0,5):
        # get a random start and end node
        start = random.choice(list(stations.values()))
        end = random.choice(list(stations.values()))
        # get the path
        data = Engine.get(start, end)

        print("Suggested Route: ", data["route"])
        print("Total Cost: ", data["cost"])
        print("Interchange times: ", data["interchange"])
        print("Suggested Line: ", data["line"])
        print("Estimate walking time is: ", data["walking"])
        print("")

if __name__ == "__main__":
    main()

    
   