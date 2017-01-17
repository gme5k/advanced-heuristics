from nationLoader import *
from scoreFunction import *
from jsonDeepCopy import *

provinces = []
numTransmitters = 4
index = 0
costs = 0
transmitterCosts = [20, 22, 28, 32, 37, 39, 41]


def branchNBound(nationtxt, bound):
    global index
    nation = nationLoader(nationtxt)

    for key in nation:
        provinces.append(key)

    upperbound = bound

    solution = []

    while True:
        if index == -1:
            break

        if nation[provinces[index]][1] == numTransmitters:
            updateTransmitter(nation, True)
            continue
        else:
            updateTransmitter(nation, False)

        # Costs
        # costs = scoreFunction(nation, 1)[0]
        if (costs + (len(provinces) - (index + 1)) * transmitterCosts[0]) > upperbound:
            updateTransmitter(nation, True)
            continue


        # Neighbor
        conflict = False
        for neighbor in nation[provinces[index]][0]:
            if nation[neighbor][1] == nation[provinces[index]][1]:
                conflict = True
                break

        if conflict:
            continue

        # Solution
        if index == len(provinces) - 1:
            print "SOLUTION:"
            if costs < upperbound:
                solution = []
            solution.append(json_deep_copy(nation))
            upperbound = costs
            updateTransmitter(nation, True)
            print upperbound
            print nation
            continue

        index += 1

    print solution
    print upperbound
    print len(solution)


def updateTransmitter(nation, previous):
    global index
    global costs
    if previous:
        costs = costs - transmitterCosts[nation[provinces[index]][1] - 1]
        print nation[provinces[index - 1]][1]
        #deduct =  transmitterCosts[nation[provinces[index - 1]][1] - 1]
        costs -= 20
        #costs -= transmitterCosts[nation[provinces[index - 1]][1] - 1]
        nation[provinces[index]][1] = 0
        index -= 1

    else:
        nation[provinces[index]][1] += 1
        costs += transmitterCosts[nation[provinces[index]][1] - 1]




branchNBound("TXT/Nederland.txt", 600)
