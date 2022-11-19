from Data import * 

class Engine:
    # for checking if the line is changed
    def __checkChangeLine(self, curLine, curNode, nextNode, fromLine):
        if len(curLine) == 0:
            return True
        if curLine[-1] == fromLine:
            return False
        if fromLine == "Walking":
            return True
        if curLine[-1] == "Tung Chung Line" and curNode in airportLine2 and nextNode in airportLine2:
            return True
        if curLine[-1] not in node_lines[nextNode]:
            return True
        else:
            return False

    # for finding the walking time when changing line
    def __findWalkingTime(self, curNode, toLine):
        try:
            if toLine == "Walking" or toLine == "":
                return 0

            for i in change_lines_time[curNode]:
                l = dict(i)
                if l["to"] == toLine:
                    return l['time']
        except KeyError:
            return 0

    # for finding the walking time when changing line
    def __findWaitingTime(self, toLine):
        try:
            if toLine == "Walking":
                return 0
            
            # print("waiting: ", expectWaitTime[toLine])
            return expectWaitTime[toLine]
        except KeyError:
            return 0

    # using A* search algorithm for finding the shortest path
    def __A_star(self, graph, costs, open, closed, cur_node, heuristic, totalcosts, line, total_walkTime, stations, smallcost):
        if cur_node in open:
            open.remove(cur_node)

        closed.add(cur_node)
        for i in graph:
            walktime = 0
            waittime = 0
            if (i[0] == cur_node and costs[i[0]][0]+i[2]+heuristic[i[0]] < (costs[i[1]][0]+costs[i[1]][1]) and i[1] not in closed):
                open.add(i[1])
                if(costs[i[0]] == 0):
                    waittime = self.__findWaitingTime(i[3])
                if(len(line[i[0]]) == 0):
                    line[i[0]].append(i[3])
                next_line = line[i[0]].copy()
                if (self.__checkChangeLine(line[i[0]], i[0], i[1], i[3])):
                    waittime += self.__findWaitingTime(i[3])
                    walktime = self.__findWalkingTime(i[0], i[3])
                    if i[3] == line[i[0]][-1]:
                        pass
                    else:
                        next_line.append(i[3])
                line[i[1]] = next_line
                # print("worktime", walktime)
                # add the walking time when changing line
                if walktime is None:
                    # store the cost
                    costs[i[1]][0] = costs[i[0]][0]+i[2]

                else:
                    # store the total walking time
                    if i[3] == "Walking":
                        total_walkTime[i[1]] = total_walkTime[i[0]] + i[2]
                    else:
                        total_walkTime[i[1]] = total_walkTime[i[0]] + walktime

                    # store the cost with walking time
                    costs[i[1]][0] = costs[i[0]][0] + i[2] + walktime + waittime
                    # store the heurisitc of current node
                    costs[i[0]][1] = heuristic[i[0]]+walktime

                # store the path
                if stations[i[1]] == self.path[i[0]].split(' -> ')[-1]:
                    self.path[i[1]] = self.path[i[0]]
                else:
                    self.path[i[1]] = self.path[i[0]] + ' -> ' + stations[i[1]]
                # store the heurisitc of next node
                costs[i[1]][1] = heuristic[i[1]]
                # store the total cost
                totalcosts[i[1]] = costs[i[1]][0]

                # smallest cost
                smallcost[i[1]] = sum(costs[i[1]])
                # print(path[i[1]], totalcosts[i[1]])

        # find the node with the lowest cost
        smallcost[cur_node] = 999999
        small = min(smallcost, key=smallcost.get)
        # print("smallest node", stations[small])
        if small not in closed:
            self.__A_star(graph, costs, open, closed, small, heuristic,
                totalcosts, line, total_walkTime, stations, smallcost)
    
    def get(self, start_str, end_str):
        costs = dict()  # for storing the cost of each node for the program process
        self.path = dict()  # for storing the path
        totalcosts = dict()  # for storing the total cost of the path
        line = dict()  # for storing the subway line of the path
        total_walkTime = dict()  # for storing the total walking time of the path
        smallcost = dict()  # for storing the sum of the cost and heuristic of the node
        for i in nodes:
            # costs array contain the distance and the heurisitc of current node
            costs[i] = [999999, 0]
            self.path[i] = ' '
            totalcosts[i] = 999999
            line[i] = []
            total_walkTime[i] = 0
            smallcost[i] = 999999
        open = set()
        closed = set()

        # initial the data
        start_node_str = start_str
        start_node = list(stations.keys())[list(
            stations.values()).index(start_node_str)]
        open.add(start_node)
        self.path[start_node] = start_node_str
        costs[start_node] = [0, 0]
        totalcosts[start_node] = 0
        total_walkTime[start_node] = 0
        smallcost[start_node] = 0

        goal_node_str = end_str
        if start_node_str in airportLine1 and goal_node_str in lines["Airport Express"]:
            goal_node = list(airportLine2Value.keys())[list(
                airportLine2Value.values()).index(goal_node_str)]
        elif start_node_str in airportLine2 and goal_node_str in airportLine1:
            goal_node = list(airportLine1Value.keys())[list(
                airportLine1Value.values()).index(goal_node_str)]
        else:
            goal_node = list(stations.keys())[list(
                stations.values()).index(goal_node_str)]

        h = heuristics[goal_node]
        # program start
        self.__A_star(graph, costs, open, closed, start_node,
            h, totalcosts, line, total_walkTime, stations, smallcost)
        return {
            "route": self.path[goal_node],
            "interchange": len(line[goal_node])-1,
            "line": line[goal_node],
            "cost": totalcosts[goal_node],
            "walking": total_walkTime[goal_node]
        }