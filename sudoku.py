import numpy
import random
myNumber = 9
def readSudoku():
    mainSudoku = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
                  [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    return mainSudoku

def makePopulations(mainSudoko): #jamiate avvalie ra misazad
    board = [[]]
    for i in range(myNumber-1):
        board.append([])
    for i in range(myNumber):
        for j in range(myNumber):
            board[i].append([])
    #yek board 9*9 misazad k dar har khane yek array ast va dar har array adadi k 3 shart ra darad mizarad
    for i in range(myNumber):
        for j in range(myNumber):
            for k in range(1,myNumber+1):
                if(mainSudoko[i][j] == 0):
                    if(not(rowDup(mainSudoko,i,k) or columnDup(mainSudoko,j,k) or subBlockDup(mainSudoko,i,j,k))):
                        board[i][j].append(k)
                else:
                    board[i][j].append(mainSudoko[i][j])
                    break
    #1000 cromosome tolid mikonad
    populations = []
    for p in range(1000):
        person = [[]]
        for i in range(myNumber - 1):
            person.append([])
        for i in range(myNumber):  #yek satre jadid k hmeie adadash dar ebteda 0 ast
            row = numpy.zeros(myNumber,dtype=int)
            for j in range(myNumber):
                if (mainSudoko[i][j] == 0): #agar meghdar na maloom bashad az beine adade valid yeki ra random entekhab mikonad
                    row[j] = int(board[i][j][random.randint(0, len(board[i][j]) - 1)])
                else:
                    row[j] = mainSudoko[i][j]

            while (len(list(set(row))) != myNumber): #rowduplicate vojood nadashte bashe
                for j in range(0, myNumber):
                    if (mainSudoko[i][j] == 0):
                        row[j] = int(board[i][j][random.randint(0, len(board[i][j]) - 1)])

            person[i] = row # har row ra set mikonad

        populations.append(person) # har cromosome sakhte shode ra b jamiat ezafe mikonad

    return populations,updateFit(populations) #yek array az population
                                              #yek array b soorate tuple (population,fitness population ha barmigardoonim

def updateFit(populations):
    puplefit = []
    for puple in populations: #baraie har ozv fitness ra b tuple add krdim
        puplefit.append(tuple((puple,findFitness(puple))))
    return puplefit

def mutation(mutationRate,mainSudoku,candidate): #dar yek satr do adad dar column haie motefavet ra ja b ja mikonad
    myrandNum = random.uniform(0, 1.1)

    mutationDone = False
    if (myrandNum < mutationRate):
        while (not mutationDone):#mutation anjam shavad
            chosenRow = random.randint(0, 8)

            firstColumn = 0
            secondColumn = 0

            while (firstColumn == secondColumn): #do sotoone motefavet entekhab mikonad
                firstColumn = random.randint(0, 8)
                secondColumn = random.randint(0, 8)

            #check mikonim k joze value haie aslimoon nabashn
            if (mainSudoku[chosenRow][firstColumn] == 0 and mainSudoku[chosenRow][secondColumn] == 0):
                #check mikonim k duplication ijad nashe
                if (not columnDup(mainSudoku,secondColumn, candidate[chosenRow][firstColumn])
                        and not columnDup(mainSudoku,firstColumn, candidate[chosenRow][secondColumn])
                        and not subBlockDup(mainSudoku,chosenRow, secondColumn, candidate[chosenRow][firstColumn])
                        and not subBlockDup(mainSudoku,chosenRow, firstColumn, candidate[chosenRow][secondColumn])):
                    #az an satr 2 sotoon ra ja b ja miknd
                    temp = candidate[chosenRow][secondColumn]
                    candidate[chosenRow][secondColumn] = candidate[chosenRow][firstColumn]
                    candidate[chosenRow][firstColumn] = temp
                    mutationDone = True

    return

def crossOver(crossoverRate,firstParent,secondParent):

    firstChild = numpy.copy(firstParent)
    secondChild = numpy.copy(secondParent)

    myrandNum = random.uniform(0, 1.1)

    first = 2
    second = 1
    if(myrandNum < crossoverRate):
        while(first > second): #first hatman bozorgtar az second ast
            first = random.randint(0,8)
            second = random.randint(1,9)

        for i in range(first, second): #az first ta sec ra crossover mikonim
            firstChild[i], secondChild[i] = crossoverRows(firstChild[i], secondChild[i])

    return firstChild,secondChild

def crossoverRows(firstRow, secondRow):
    firstChildRow = numpy.zeros(myNumber,dtype=int)
    secondChildRow = numpy.zeros(myNumber,dtype=int)

    myCycle = list(range(1, myNumber + 1)) #
    cycle = 0

    while ((0 in firstChildRow) and (0 in secondChildRow)): #ta zamani k hnooz onsori mande bashad
        if (cycle % 2 == 0):
            index = findinCycle(firstRow,myCycle)
            start = firstRow[index]
            myCycle.remove(firstRow[index]) #az cycle an ra remove mikonim
            #zamani k cycle zoj ast baraie firstChild va secondChild haman index first va sec ra gharar midahim
            firstChildRow[index] = firstRow[index]
            secondChildRow[index] = secondRow[index]
            next = secondRow[index]

            while (next != start): #ta zamani k b start dar array dovom narecdim
                index = findVal(firstRow, next)
                myCycle.remove(firstRow[index])
                firstChildRow[index] = firstRow[index]
                secondChildRow[index] = secondRow[index]
                next = secondRow[index]

            cycle += 1
        #dar soorati k cycle fard bashad bar axe halate zoj index firstRow baraie secondChildRow va
        #index secondRow baraie firstChildRow ast
        else:
            index = findinCycle(firstRow, myCycle)
            start = firstRow[index]
            myCycle.remove(firstRow[index])
            firstChildRow[index] = secondRow[index]
            secondChildRow[index] = firstRow[index]
            next = secondRow[index]

            while (next != start):#ta zamani k b start dar array dovom narecdim
                index =findVal(firstRow, next)
                myCycle.remove(firstRow[index])
                firstChildRow[index] = secondRow[index]
                secondChildRow[index] = firstRow[index]
                next = secondRow[index]

            cycle += 1

    return firstChildRow, secondChildRow

def findinCycle(row, myCycle): #avvali addai k dar row hast k dar cycle hm hast
    for i in range(0, len(row)):
        if (row[i] in myCycle):
            return i


def findVal(row, value): #index value dar row ra barmigardanad
    for i in range(0, len(row)):
        if (row[i] == value):
            return i


def findFitness(person):
    rowArray = numpy.zeros(myNumber,dtype=int)
    columnArray = numpy.zeros(myNumber,dtype=int)
    blockArray = numpy.zeros(myNumber,dtype=int)
    rowFit = 0
    columnFit = 0
    blockFit = 0

    for i in range(myNumber):
        for j in range(myNumber):
            rowArray[person[i][j] - 1] += 1 #dar har index tedad an index dar row ra gharar midahim
        rowFit += (1.0 / len(set(rowArray)))/myNumber
        rowArray = numpy.zeros(myNumber,dtype=int)

    for i in range(myNumber):
        for j in range(myNumber):
            columnArray[int(person[j][i]) - 1] += 1 #dar har index tedad an index dar column ra gharar midahim
        columnFit += (1.0 / len(set(columnArray)))/myNumber
        columnArray = numpy.zeros(myNumber,dtype=int)

    for i in range(0,myNumber,3):
        for j in range(0,myNumber,3): #dar har index tedad an index dar subblock ra gharar midahim
            blockArray[int(person[i][j] - 1)] += 1
            blockArray[int(person[i][j + 1] - 1)] += 1
            blockArray[int(person[i][j + 2] - 1)] += 1

            blockArray[int(person[i + 1][j] - 1)] += 1
            blockArray[int(person[i + 1][j + 1] - 1)] += 1
            blockArray[int(person[i + 1][j + 2] - 1)] += 1

            blockArray[int(person[i + 2][j] - 1)] += 1
            blockArray[int(person[i + 2][j + 1] - 1)] += 1
            blockArray[int(person[i + 2][j + 2] - 1)] += 1

            blockFit += (1.0 / len(set(blockArray))) / myNumber
            blockArray = numpy.zeros(myNumber,dtype=int)

    if (int(rowFit) == 1 and int(columnFit) == 1 and int(blockFit) == 1): #dar in sharaiet behtarin fitness ra darad
        fitness = 1.0
    else: #chon rowfit = 1 ast
        fitness = columnFit * blockFit

    return fitness


def columnDup(mainSudoku,columnNum,value): #aya dar yek column duplicate vojood darad
    for i in range(myNumber):
        if(mainSudoku[i][columnNum] == value):
            return True
    return False

def rowDup(mainSudoku,rowNum,value):#aya dar yek row duplicate vojood darad
    for i in range(myNumber):
        if(mainSudoku[rowNum][i] == value):
            return True
    return False

def subBlockDup(mainSudoku,rowNum,columnNum,value):#aya dar yek subblock duplicate vojood darad
    rowNum = 3 * (int(rowNum / 3))
    columnNum = 3 * (int(columnNum / 3))

    if ((mainSudoku[rowNum][columnNum] == value)
            or (mainSudoku[rowNum][columnNum + 1] == value)
            or (mainSudoku[rowNum][columnNum + 2] == value)
            or (mainSudoku[rowNum + 1][columnNum] == value)
            or (mainSudoku[rowNum + 1][columnNum + 1] == value)
            or (mainSudoku[rowNum + 1][columnNum + 2] == value)
            or (mainSudoku[rowNum + 2][columnNum] == value)
            or (mainSudoku[rowNum + 2][columnNum + 1] == value)
            or (mainSudoku[rowNum + 2][columnNum + 2] == value)):
        return True
    else:
        return False

def populationSort(populations): #tuple k dar an fitness ra darim bar asase fitness sort mikonim

    sortedPopulations = sorted(populations, key=lambda tup: tup[1])
    sortedPopulations.reverse()
    return sortedPopulations

def compete(sortedPopulations): #yek ozve random az population bar migardanad
    #2 ozve random entekhab mikonad
    firstParent = sortedPopulations[random.randint(0, len(sortedPopulations) - 1)]
    secondParent = sortedPopulations[random.randint(0, len(sortedPopulations) - 1)]

    firstFit = findFitness(firstParent)
    secondFit = findFitness(secondParent)

    if (firstFit > secondFit):
        better = firstParent
        worse = secondParent
    else:
        better = secondParent
        worse = firstParent

    selection_rate = 0.85
    myRandNum = random.uniform(0, 1)
    if (myRandNum < selection_rate): #dar in soorat behtar ra barmigardanad az beine 2 random
        return better
    else:
        return worse

def solve(mainSudoku):
    #initial khode sudoku ha
    #initialFit yek array az tuple ha k ozve avval tupple sudoku va ozve dovom Fitness ast
    initial,initialFit = makePopulations(mainSudoku)

    for generation in range(0, 1000): #1000 nasl tolid mikonad
        sortedPopulations = populationSort(initialFit)
        if(int(sortedPopulations[0][1]) == 1):#agar behtarin dar jamiat yek bashad an ra barmigardanad
            return sortedPopulations[0][0]


        theBests = []
        bestsCount = 20
        nextPopulation = []

        for i in range(0, bestsCount): #20 taie behtar ra dar theBests mirizad
            theBests.append(numpy.copy(sortedPopulations[i]))

        for count in range(bestsCount, 1000, 2):
            #har bar 2 ozv entekhab mikonad
            firstparent = compete(initial)
            secondparent = compete(initial)

            #2 farzand ra ba crossover ijad mikonad
            firstchild, secondchild = crossOver(1,firstparent,secondparent)

            #rooie har 2 mutation anjam midahad
            mutation(.15,mainSudoku,firstchild)
            mutation(.15,mainSudoku,secondchild)
            #bacheha ra b population jadid ezafe mikonad
            nextPopulation.append(firstchild)
            nextPopulation.append(secondchild)


        for i in range(0,bestsCount):#20 taie behtar ra b jamiat ezafe mikonad
            nextPopulation.append(theBests[i][0])

        initial = nextPopulation
        initialFit = updateFit(nextPopulation) #fitness an ha ra hesab krde dar array k az tuple ha ast mirzad



print(solve(readSudoku()))
