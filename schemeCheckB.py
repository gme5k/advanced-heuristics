from random import *
import json
from nationLoader import *
from jsonDeepCopy import *
from randScoreFunction import *
from scoreFunction import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.font_manager as fm
import matplotlib.lines as mlines



lfs = fm.FontProperties(size=11)
alf = 11
lw1 = 0.5
lw2 = 3
red_line = mlines.Line2D([], [], color='red', linestyle = '-', linewidth = lw2)
magenta_line = mlines.Line2D([], [], color='magenta', linewidth = lw2)
black_line = mlines.Line2D([], [], color='black', linewidth = lw2)

f = open('writefile', 'w')
def greedyRandom(nationtxt):
    '''
    Shuffle list of provinces and loop over this list and assign transmitters

    Uncomment all ### to visualize in steps
    '''
    ### stepcounter = 0

    while True:
        #Buiten try loop
        provinceNames = []
        nation = nationLoader("TXT/" + nationtxt)

        for province in nation:
            provinceNames.append(province)

        try:
            # Randomly shuffle list of province names
            shuffle(provinceNames)


            for province in provinceNames:
                transmitterOptions = [1, 2, 3, 4]

                # If province has no neighbours then assign transm 1
                if not nation[province][0]:
                    nation[province][1] = 1
                elif nation[province][1] == 0:
                    # remove neighbor transmitters from options
                    for neighbor in nation[province][0]:
                        if nation[neighbor][1] in transmitterOptions:
                            transmitterOptions.remove(nation[neighbor][1])

                    # select first transmitter from options and assign it
                    transmitter = transmitterOptions[0]
                    nation[province][1] = transmitter

                    ### stepcounter = stepcounter + 1
                    ### jsonPath = "JSON/" + nationtxt[:-4] + "/Step" + str(stepcounter) + ".txt"
                    ### json.dump(nation, open(jsonPath,'w'))
            break

        except:
            pass

    return nation

def sgap(gap):
    a = 1
    b = a + gap
    c = a + 1 + gap
    d = a + 2 + gap
    e = a + 3 + gap
    f = a + 4 + gap
    g = a + 5 + gap
    scheme =[a, b, c, d, e, f, g]
    return scheme, gap

def multigap(gap):
    a = 1
    b = 2
    c = b + gap
    d = c + gap
    e = d + gap
    f = e + gap
    g = f + gap

    scheme = [a, b, c, d, e, f, g]

    return scheme, gap
def Repeater(algorithm, runs, nationtxt, schemeIn):
    """
    Show distribution plot of algorithm

    Arguments
    ----------
    algorithm:  algorithm you want used
    runs:       number of trials chosen
    nationtxt:  name of nation text file
    updateFreq: Gives update after updateFreq number of runs
    plot:       'y' or 'n' for yes or no to plot. Standard is 'y'
    """

    scores = {}

    # Make sure appropriate range is used for scores

    scoreRange = range(0, 10000)

    # score range has to be between these two numbers
    for i in scoreRange:
        scores.update({i : 0})

    #~ print "Running " + str(algorithm)[0:-18] + "> " + str(runs) + " times...\n"


    minScore = 10**40


    scheme = schemeIn
    avg = (scheme[0] + scheme[1] + scheme[2] + scheme[3] + scheme[4] + scheme[5] + scheme[6]) / 7.
    p0 = (scheme[0] - avg)**2
    p1 = (scheme[1] - avg)**2
    p2 = (scheme[2] - avg)**2
    p3 = (scheme[3] - avg)**2
    p4 = (scheme[4] - avg)**2
    p5 = (scheme[5] - avg)**2
    p6 = (scheme[6] - avg)**2
    var = (p0 + p1 + p2 + p3 + p4 + p5 + p6) / 7.
    sDev = var**0.5


    q0 = scheme[1] - scheme[0]
    q1 = scheme[2] - scheme[1]
    q2 = scheme[3] - scheme[2]
    q3 = scheme[4] - scheme[3]
    q4 = scheme[5] - scheme[4]
    q5 = scheme[6] - scheme[5]

    for i in range(runs):
        nation = algorithm(nationtxt)

        score = randScoreFunction(nation, scheme)
        scores[score] += 1

        # keep track of best scores and nation
        if score < minScore:
            minScore = score
            bestNation = nation

    maxFreq = 0

    scoreCount = 0

    for score in scores:
        if scores[score] > maxFreq:
            maxFreq = scores[score]
            maxFreqScore = score
        if score == minScore:
            minScoreFreq = scores[score]
        if scores[score] >= 1:
            scoreCount += 1


    usedTrans = []
    fivePlus = 0
    fivePlusNoDuplicate = 0

    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0

    for province in bestNation:

        if bestNation[province][1] == 1:
            one += 1
        if bestNation[province][1] == 2:
            two += 1
        if bestNation[province][1] == 3:
            three += 1
        if bestNation[province][1] == 4:
            four += 1
        if bestNation[province][1] == 5:
            five += 1
        if bestNation[province][1] == 6:
            six += 1
        if bestNation[province][1] == 7:
            seven += 1


    if five > 0 or six > 0 or seven > 0:
        fivePlus += 1
        if scheme[3] != scheme[4]:
            fivePlusNoDuplicate += 1

    usedTrans.append([one, two, three, four, five, six, seven])


    return minScore, minScoreFreq, scheme, fivePlus, fivePlusNoDuplicate, usedTrans, scoreCount, sDev, q0, q1, q2, q3, q4, q5, avg





def branchNBound(nationtxt, bound, scheme):

    """
    Depth first, check upper bound and neighbors
    """
    provinces = []
    index = 0
    costs = 0
    numTransmitters = 7

    transmitterCosts = scheme
    nation = nationLoader(nationtxt)


    neighborCount = {}
    for province in nation:
        neighborCount.update({province:len(nation.get(province)[0])})


    #~ neighborCountSorted = sorted(neighborCount, key=neighborCount.__getitem__)

    neighborCountSorted = sorted(neighborCount, key=neighborCount.__getitem__, reverse=True)

    for key in neighborCountSorted:
        provinces.append(key)
    #~ print provinces

    upperbound = bound
    #~ print bound
    #~ print bound



    solution = []


    counter = 0





    while index >= 0:


        counter += 1
        if counter % 100000000 == 0:
            print counter
            print "Now at:", nation


        if index == -1:
            break

        # Assign transmitter
        if nation[provinces[index]][1] == numTransmitters:
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        else:
            costs, index = updateTransmitter(nation, False, scheme, provinces, costs, index)

        # Check if costs are above upper bound
        if (costs + (len(provinces) - (index + 1)) * transmitterCosts[0]) > upperbound:
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        # Check if a neighbor has the same transmitter
        conflict = False
        for neighbor in nation[provinces[index]][0]:
            if nation[neighbor][1] == nation[provinces[index]][1]:
                conflict = True
                break

        if conflict:
            continue

        # Check if a solution is found
        if index == len(provinces) - 1:
            #~ print "\nSOLUTION:"
            if costs < upperbound:
                solution = []
            solution.append(json_deep_copy(nation))
            upperbound = costs
            #~ print "Score:", upperbound
            #~ print nation
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        index += 1


    usedTrans = []
    fivePlus = 0
    fivePlusNoDuplicate = 0

    for nation in solution:

        one = 0
        two = 0
        three = 0
        four = 0
        five = 0
        six = 0
        seven = 0

        for province in nation:

            if nation[province][1] == 1:
                one += 1
            if nation[province][1] == 2:
                two += 1
            if nation[province][1] == 3:
                three += 1
            if nation[province][1] == 4:
                four += 1
            if nation[province][1] == 5:
                five += 1
            if nation[province][1] == 6:
                six += 1
            if nation[province][1] == 7:
                seven += 1


        if five > 0 or six > 0 or seven > 0:
            fivePlus += 1
            if transmitterCosts[3] != transmitterCosts[4]:
                fivePlusNoDuplicate += 1

        usedTrans.append([one, two, three, four, five, six, seven])

    return fivePlus, fivePlusNoDuplicate, usedTrans, upperbound, len(solution), counter
        #~ f.write("\n Used Transmitters: "+ str(one)+" "+ str(two)+" "+ str(three)+" "+ str(four)+" "+ str(five)+" "+ str(six)+" "+ str(seven)+"\n Cost: "+str(upperbound)+"\n Number of solutions: "+str(len(solution))+"\n Iterations: "+str(counter)+"\n"+"\n"+"\n"+"\n")

        #~ print "transmitter frequecies:", one, two, three, four, five, six, seven
        #~ print "Solutions:", solution
        #~ print "Cost:", upperbound
        #~ print "Number of solutions:", len(solution)
        #~ print "Iterations:", counter

def branchNBound2(nationtxt, bound, scheme):

    """
    Depth first, check upper bound and neighbors
    """


    nation = nationLoader(nationtxt)
    transmitterCosts = scheme

    neighborCount = {}
    for province in nation:
        neighborCount.update({province:len(nation.get(province)[0])})


    neighborCountSorted = sorted(neighborCount, key=neighborCount.__getitem__)

    #~ neighborCountSorted = sorted(neighborCount, key=neighborCount.__getitem__, reverse=True)

    for key in neighborCountSorted:
        provinces.append(key)
    #~ print provinces

    upperbound = bound
    #~ print bound



    solution = []


    counter = 0




    while index >= 0:

        counter += 1
        if counter % 100000000 == 0:
            print counter
            print "Now at:", nation


        if index == -1:
            break

        # Assign transmitter
        if nation[provinces[index]][1] == numTransmitters:
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        else:
            costs, index = updateTransmitter(nation, False, scheme, provinces, costs, index)

        # Check if costs are above upper bound
        if (costs + (len(provinces) - (index + 1)) * transmitterCosts[0]) > upperbound:
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        # Check if a neighbor has the same transmitter
        conflict = False
        for neighbor in nation[provinces[index]][0]:
            if nation[neighbor][1] == nation[provinces[index]][1]:
                conflict = True
                break

        if conflict:
            continue

        # Check if a solution is found
        if index == len(provinces) - 1:
            #~ print "\nSOLUTION:"
            if costs < upperbound:
                solution = []
            solution.append(json_deep_copy(nation))
            upperbound = costs
            #~ print "Score:", upperbound
            #~ print nation
            costs, index = updateTransmitter(nation, True, scheme, provinces, costs, index)
            continue

        index += 1



    usedTrans = []
    fivePlus = 0
    fivePlusNoDuplicate = 0

    for nation in solution:

        one = 0
        two = 0
        three = 0
        four = 0
        five = 0
        six = 0
        seven = 0

        for province in nation:

            if nation[province][1] == 1:
                one += 1
            if nation[province][1] == 2:
                two += 1
            if nation[province][1] == 3:
                three += 1
            if nation[province][1] == 4:
                four += 1
            if nation[province][1] == 5:
                five += 1
            if nation[province][1] == 6:
                six += 1
            if nation[province][1] == 7:
                seven += 1


        if five > 0 or six > 0 or seven > 0:
            fivePlus += 1
            if transmitterCosts[3] != transmitterCosts[4]:
                fivePlusNoDuplicate += 1

        usedTrans.append([one, two, three, four, five, six, seven])

    return counter
def kostenschema():
    kostenschemalen = 7
    schema = []

    for i in range(kostenschemalen):
        x = random.randint(1,50)

        schema.append(x)



    schema.sort()

    return schema

def updateTransmitter(nation, previous, scheme, provinces, costs, index):
    """
    Assign transmitter and update costs
    """

    transmitterCosts = scheme


    # Subtract costs of current transmitter from costs
    if nation[provinces[index]][1] != 0:
        costs -= transmitterCosts[nation[provinces[index]][1] - 1]

    # If previous, set transmitter f current province to 0 and set index to previous province
    if previous:

        nation[provinces[index]][1] = 0
        index -= 1

    # Else, assign next transmitter to province and update costs
    else:
        nation[provinces[index]][1] += 1
        costs += transmitterCosts[nation[provinces[index]][1] - 1]

    return costs, index

def sorter(a, b):
    af = []
    bf = []
    
    dic = {}
    
    for i in range(len(a)):
        dic.update({a[i]:b[i]})
    
    for key, value in sorted(dic.iteritems()):
        af.append(key)
        bf.append(value)
    return af, bf
    
def avgr(diffs, iters):
   
    uniqueDiffs = []
    avgIters = []
    
    diffsFinal = []
    itersFinal = []
    
    
    for i in range(0, len(diffs)):
        som = iters[i]
        count = 1
        
        if diffs[i] not in uniqueDiffs:
            uniqueDiffs.append(diffs[i])
            
            for j in range(i + 1, len(diffs)):
                
                if diffs[j] == diffs[i]:
                    som += iters[j]
                    count += 1
                
            
            avg = float(som) / count
            avgIters.append(avg)
    
    diffAvg = {}
    diffAvgSorted = {}
    
    for i in range(len(avgIters)):
        diffAvg.update({uniqueDiffs[i]: avgIters[i]})
    #~ print diffAvg
    
    #~ for key in sorted(diffAvg.iterkeys()):
        #~ diffAvgSorted.update({key: diffAvg[key]})
    
    #~ print diffAvg
    #~ print diffAvgSorted
    
    for key, value in sorted(diffAvg.iteritems()):
        diffsFinal.append(key)
        itersFinal.append(value)

        
    return diffsFinal, itersFinal


    
        

def main(reps, doubleBranch):
    h = 1
    maxIterations = 0
    minIterations = 10**20
    fivePlusCount = 0
    fivePlusNoDuplicateCount = 0
    fivePlusCountG = 0
    fivePlusNoDuplicateCountG = 0
    hardestScheme = 0
    easiestScheme = 0
    hardestSchemeG = 0
    curMinScoreFreq = 10000
    greedyFail = 0
    maxSDev = 0
    minSDev = 0
    sDevl = []
    iterl = []
    schemesComplete = []
    iterl2 = []

    q0l = []
    q1l = []
    q2l = []
    q3l = []
    q4l = []
    q5l = []
    
    q0avg = []
    q1avg = []
    q2avg = []
    q3avg = []
    q4avg = []
    q5avg = []
    gapl = []
    gapl2 = []
    
    avgl = []
    scorel = []
   

    


    for i in range(reps):

        print h
        provinces = []
        index = 0
        costs = 0
        numTransmitters = 7
        if i < 26:
            schemeIn, gap = multigap(i)
        else:
            schemeIn, gap2 = sgap(i - 26)


        bound, minScoreFreq, scheme, fivePlusG, fivePlusNoDuplicateG, usedTransG, scoreCount, sDev, q0, q1, q2, q3, q4, q5, avg = Repeater(greedyRandom, 10000, "Nederland.txt", schemeIn)
        fivePlus, fivePlusNoDuplicate, usedTransmitters, lowCost, nSolutions, iterations = branchNBound("TXT/Nederland.txt", bound, scheme)



        if doubleBranch == 1:
            iterations2 = branchNBound2("TXT/Nederland.txt", bound, scheme)
            iterl2.append(iterations2)
        if i < 26: 
            gapl.append(gap)
            iterl.append(iterations)
        else:
            gapl2.append(gap2)
            iterl2.append(iterations)
        sDevl.append(sDev)
    
            
        schemesComplete.append(scheme)
        avgl.append(avg)
        scorel.append(lowCost)
        
        q0l.append(q0)
        q1l.append(q1)
        q2l.append(q2)
        q3l.append(q3)
        q4l.append(q4)
        q5l.append(q5)
        

        
        

        fivePlusCount += fivePlus
        fivePlusNoDuplicateCount += fivePlusNoDuplicate

        fivePlusCountG += fivePlusG
        fivePlusNoDuplicateCountG += fivePlusNoDuplicateG

        if lowCost != bound:
            greedyFail += 1

        print "iterations",iterations

        if doubleBranch == 1:
            print iterations2

        if doubleBranch != 1:
            if iterations > maxIterations:
                maxIterations = iterations
                hardestScheme = scheme
                maxSDev = sDev


                f.write("\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost: "+str(avg)+"\n\n lowest score branch and bound: "+str(lowCost)+
                "\n lowest score greedy: "+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")

                print "\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost: "+str(avg)+"\n\n lowest score branch and bound: "+str(lowCost)+"\n lowest score greedy: "+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"
            if iterations < minIterations:
                minIterations = iterations
                easiestScheme = scheme
                minSDev = sDev

                f.write("\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost: "+str(avg)+"\n\n lowest score branch and bound: "+str(lowCost)+
                "\n lowest score greedy: "+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")

                print "\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost: "+str(avg)+"\n\n lowest score branch and bound: "+str(lowCost)+"\n lowest score greedy: "+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"

        #~ +"\n branchIterations2: "+str(iterations2)+
        if doubleBranch == 1:
            if iterations2 > maxIterations:
                maxIterations = iterations2
                hardestScheme = scheme
                maxSDev = sDev

                f.write("\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+
                "\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")
                print "\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+"\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"
            if iterations > maxIterations:
                maxIterations = iterations
                hardestScheme = scheme
                maxSDev = sDev


                f.write("\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+
                "\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")
                print "\n HARD "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+"\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"


            if iterations < minIterations:
                minIterations = iterations
                easiestScheme = scheme
                minSDev = sDev


                f.write("\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+
                "\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")
                print "\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+"\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"
            if iterations2 < minIterations:
                minIterations = iterations2
                easiestScheme = scheme
                minSDev = sDev

                f.write("\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+
                "\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+
                "\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+
                "\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+
                "\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n")
                print "\n EASY "+"\n Scheme: "+str(scheme)+"\n transmitter type cost standard deviation: "+str(sDev)+"\n average transitter type cost"+str(avg)+"\n\n lowest score branch and bound"+str(lowCost)+"\n lowest score greedy"+str(bound)+"\n\n branch and bound iterations: "+str(iterations)+"\n\n branch and bound iterations 2: "+str(iterations2)+"\n branch and bound amount of solutions: "+str(nSolutions)+"\n branch and bound used transmitter types: "+str(usedTransmitters)+"\n\n instances used transmitter type 5+: "+str(fivePlus)+"\n instances used transmitter type 5+, no duplicate transmitter type costs: "+str(fivePlusNoDuplicate)+"\n\n\n"

        #~ if minScoreFreq < curMinScoreFreq:
            #~ curMinScoreFreq = minScoreFreq
            #~ hardestSchemeG = scheme
            #~ print "greedy"
            #~ f.write("\n greedy")
            #~ f.write("\n Scheme: "+str(scheme)+"\n sDev: "+str(sDev)+"\n\n greedyLowestCost: "+str(bound)+"\n minScoreFreq: "+str(minScoreFreq)+"\n scoreCount: "+str(scoreCount)+"\n greedyUsedTrans"+str(usedTransG)+"\n greedyFivePlus: "+str(fivePlusG)+"\n greedyFivePlusNoDuplicate: "+str(fivePlusNoDuplicateG)+"\n\n branchLowestCost: "+str(lowCost)+"\n branchIterations: "+str(iterations)+"\n branchIterations2: "+str(iterations2)+"\n branchNSolutions: "+str(nSolutions)+"\n branchTransUsed: "+str(usedTransmitters)+"\n fivePlus: "+str(fivePlus)+"\n fivePlusNoDuplicate: "+str(fivePlusNoDuplicate)+"\n\n\n")
            #~ print "\n Scheme: "+str(scheme)+"\n sDev: "+str(sDev)+"\n\n greedyLowestCost: "+str(bound)+"\n minScoreFreq: "+str(minScoreFreq)+"\n scoreCount: "+str(scoreCount)+"\n greedyUsedTrans"+str(usedTransG)+"\n greedyFivePlus: "+str(fivePlusG)+"\n greedyFivePlusNoDuplicate: "+str(fivePlusNoDuplicateG)+"\n\n branchLowestCost: "+str(lowCost)+"\n branchIterations: "+str(iterations)+"\n branchIterations2: "+str(iterations2)+"\n branchNSolutions: "+str(nSolutions)+"\n branchTransUsed: "+str(usedTransmitters)+"\n fivePlus: "+str(fivePlus)+"\n fivePlusNoDuplicate: "+str(fivePlusNoDuplicate)+"\n\n\n"

        h += 1
    
    
    
    
    
    
    schemeIters = {}
    schemeItersSorted = {}
    print "\n\n"
    
    for i in range(len(iterl)):
        schemeIters.update({iterl[i]: schemesComplete[i]})
    
        
    print "\n\n"
        
    print "schemes / iterations sorted"
    f.write("\n"+"schemes / iterations sorted")
    
    for key, value in sorted(schemeIters.iteritems()):
        print key, value
        f.write("\n"+str(key)+": "+str(value))
        
        
   
        
    print "\n\n"
    f.write("\n\n")
    
    


        
   
        
        
    f.write("\n Hardest Branch")
    print "Hardest Branch"

    f.write("\n maxIterations: "+str(maxIterations)+"\n fivePlusCount: "+str(fivePlusCount)+
    "\n fivePlusNoDuplicateCount: "+str(fivePlusNoDuplicateCount)+"\n hardestScheme: "+str(hardestScheme)+
    "\n maximum transmitter type cost standard deviation: "+str(maxSDev)+"\n\n"+"\n times lowest greedy score != lowest BnB score"+str(greedyFail))

    print "\n maxIterations: "+str(maxIterations)+"\n fivePlusCount: "+str(fivePlusCount)+"\n fivePlusNoDuplicateCount: "+str(fivePlusNoDuplicateCount)+"\n hardestScheme: "+str(hardestScheme)+"\n maximum transmitter type cost standard deviation: "+str(maxSDev)+"\n times lowest greedy score != lowest BnB score: "+str(greedyFail)+"\n\n"


    f.write("\n easiest Branch")
    print "Easiest Branch"

    f.write("\n minIterations: "+str(minIterations)+"\n fivePlusCount: "+str(fivePlusCount)+
    "\n fivePlusNoDuplicateCount: "+str(fivePlusNoDuplicateCount)+"\n easiestScheme: "+str(easiestScheme)+
    "\n minimum transmitter type cost standard deviation: "+str(minSDev)+"\n\n"+"\n times lowest greedy score != lowest BnB score"+str(greedyFail))

    print "\n minIterations: "+str(minIterations)+"\n fivePlusCount: "+str(fivePlusCount)+"\n fivePlusNoDuplicateCount: "+str(fivePlusNoDuplicateCount)+"\n easiestScheme: "+str(easiestScheme)+"\n minimum transmitter type cost standard deviation: "+str(minSDev)+"\n times lowest greedy score != lowest BnB score: "+str(greedyFail)+"\n\n"
    
    #~ print schemeIters
    #~ print schemeItersSorted
    for i in schemeItersSorted:
        f.write(str(i)+": "+str(schemeItersSorted[i])+"\n")
        print str(i)+": "+str(schemeItersSorted[i])+"\n"
    
    #~ plus = []
    #~ for i in range(len(gapl)):
        #~ plus.append(iterl[i] + iterl2[i])
        
    #~ f.write("\n Hardest Greedy")
    #~ print "Hardest Greedy"
    #~ f.write("\n curMinScoreFreq: "+str(curMinScoreFreq)+"\n fivePlusCountG: "+str(fivePlusCountG)+"\n fivePlusNoDuplicateCountG: "+str(fivePlusNoDuplicateCountG)+"\n hardestScheme: "+str(hardestSchemeG)+"\n greedyFail: "+str(greedyFail))
    #~ print "\n curMinScoreFreq: "+str(curMinScoreFreq)+"\n fivePlusCountG: "+str(fivePlusCountG)+"\n fivePlusNoDuplicateCountG: "+str(fivePlusNoDuplicateCountG)+"\n hardestScheme: "+str(hardestSchemeG)+"\n greedyFail: "+str(greedyFail)
    f.close()
    #~ gapFit = np.poly1d(np.polyfit(gapl,iterl,2))
    #~ gapFit = makeFit(gapl, popt[0], popt[1], popt[2])
    u, (ax1) = plt.subplots(1)
    #~ ax1.plot(gapl, gapFit(gapl), '--r', linewidth = lw2)
    ax1.plot(gapl, iterl, color = "black", linewidth = lw2)
    ax1.plot(gapl2, iterl2, color = 'red', linewidth = lw2)
    #~ ax1.plot(gapl, plus, color = 'green', linewidth = lw1)
    ax1.set_title("Iterations over Cost Gap Parametrization", fontsize = alf)
    ax1.set_xlabel("Cost Gap", fontsize = alf)
    ax1.set_ylabel("iterations", fontsize = alf)
    ax1.tick_params(labelsize = alf)
    ax1.set_yscale('log')
    u.legend([red_line, black_line] ,[ 'cost gap a/b', 'cost gap b/c, c/d, d/e, e/f, f/g'], bbox_to_anchor=(0.85, 0.89), prop = lfs)
    u.savefig('gap.png', bbox_inches='tight')
    
    
    #~ plotter(q0l, q1l, q2l, q3l, q4l, q5l, iterl)
    
def divide(a):
    l = []
    
    for i in a:
        if i != 0:
            p = float(1) / i
            l.append(p)
        else: 
            l.append(i)
    return l
    
def func(x, a, b, c):
    return a/float(x[0] - b) + c

def funcAlt(x, a, b, c):
    return a/float(x - b) + c
    
def makeFit(xl, a, b, c):
    l = []
    for i in xl:
        l.append(funcAlt(i, a, b, c))
    return l
    
def plotter(x1, x2, x3, x4, x5, x6, y):
    
    
    #~ x2 = divide(x2)
    #~ x3 = divide(x3)
    #~ x4 = divide(x4)
    #~ x5 = divide(x5)
    #~ x6 = divide(x6)
    
    tt = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    hh = plt.figure(figsize = (5.396  , 8.191))

    hh.clf()
    
    
    ax1 = hh.add_axes([0.04,0.1,0.44,0.2])
    ax2 = hh.add_axes([0.52,0.1,0.44,0.2])
    ax3 = hh.add_axes([0.04,0.4,0.44,0.2])
    ax4 = hh.add_axes([0.52,0.4,0.44,0.2])
    ax5 = hh.add_axes([0.04,0.7,0.44,0.2])
    ax6 = hh.add_axes([0.52,0.7,0.44,0.2])
    
    xlist = [x1, x2, x3, x4, x5, x6]
   
    axlist = [ax1, ax2, ax3, ax4, ax5, ax6]
    fitlist = []
    
    
    #~ popt, pcov= curve_fit(func, sorter(xlist[i],y)[0], sorter(xlist[i],y)[1])
    #~ fitlist.append(makefit(sorter(xlist[i],y)[0], popt[0], popt[1]))
    
    
    
    
    #~ for i in range(len(axlist)):
        #~ popt, pcov= curve_fit(func, sorter(xlist[i],y)[0], sorter(xlist[i],y)[1])
        #~ print popt[0], popt[1]
#~ plot(axlist[i], func(axlist[i])
    
    
  
    for i in range(len(axlist)):
        if i == 0:
            fitlist.append(np.poly1d(np.polyfit(sorter(xlist[i],y)[0],sorter(xlist[i],y)[1],2)))
    
            #~ fitlist.append(np.poly1d(np.polyfit(sorter(xlist[i],y)[0],sorter(xlist[i],y)[1],1)))
            #~ popt, pcov= curve_fit(func, sorter(xlist[i],y)[0], sorter(xlist[i],y)[1])
            #~ print popt
            #~ fitlist.append(makeFit(sorter(xlist[i],y)[0], popt[0], popt[1]))
            
        axlist[i].scatter(xlist[i], y, color = "black", linewidth = lw1)
        axlist[i].set_title("Transmitter "+tt[i]+"/"+tt[i+1], fontsize = alf)
        axlist[i].set_xlabel('Cost Gap', fontsize = alf)
        if i % 2 == 0:
            axlist[i].set_ylabel('Iterations', fontsize = alf)
        else:
            axlist[i].set_yticklabels([])
        axlist[i].tick_params(axis = 'both', labelsize = alf)
        axlist[i].set_xlim(0, 50)
        if i == 0:
            axlist[i].plot(sorter(xlist[i],y)[0], fitlist[i](sorter(xlist[i],y)[0]), '--r', linewidth = lw2)
       
            #~ axlist[i].plot(sorter(xlist[i],y)[0], fitlist[i], '--r', linewidth = lw2)
 
    hh.savefig('lin.png',bbox_inches='tight', dpi = 100)
    
    for i in range(len(axlist)):
        #~ axlist[i].set_yscale('log')
        if i % 2 == 0:
            axlist[i].set_ylabel('Iterations', fontsize = alf)
        else:
            axlist[i].set_yticklabels([])
        
    hh.savefig('log.png',bbox_inches='tight', dpi = 100)
    
    
   
    
  
   

#~ ____________________________________________________________________-



    
main(52, 0)
#~ print avgr([5, 5, 5, 2, 6, 7, 7, 8, 4, 6, 7, 5, 3, 2, 5, 8, 9, 5, 5, 3, 3],[5, 6, 3, 8, 4, 7, 4, 7, 8, 4, 7, 3, 1, 6, 9, 0, 5, 2, 6, 8, 7])
