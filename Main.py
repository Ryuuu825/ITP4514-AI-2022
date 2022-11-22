import Engine
from Data import * 


Engine = Engine.Engine()

def main():
    while True:
        print("Welcome to MTR Route Finder")
        print("Please enter the start station: ")
        start = input()
        print("Please enter the end station: ")
        end = input()
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

    
   