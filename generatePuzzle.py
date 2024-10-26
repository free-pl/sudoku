def circularShift(array,shift):

    array2=copy.copy(array)
    for i in range(shift):
        value=array2[0]
        del array2[0]
        array2.append(value)
    return array2



def generatePuzzle(difficulty,puzzle=[],removed=[],removecount=0,start=time.time(),deadends=0):

    #if (time.time()-start)>10:

        #raise RuntimeError

    if puzzle==[]: # this runs only on first call to generate the full solution

        removecount=random.randint(30,40)

        row=["1","2","3","4","5","6","7","8","9"] # generate valid puzzle using circular shifts
        random.shuffle(row)
        for i in range(3):
            row=circularShift(row,1)
            puzzle.append(row)
            row=circularShift(row,3)
            puzzle.append(row)
            row=circularShift(row,3)
            puzzle.append(row)

        swaps=((0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(6,7),(6,8),(7,8)) # rows/columns that can be swapped whilst staying valid
        for i in range(150): # randomly swap rows/columns to get rid of shift pattern
            roworcolumn=random.randint(1,2)
            swap=swaps[random.randint(0,len(swaps)-1)]
            
            if roworcolumn==1: # i.e. swap rows
                temp=puzzle[swap[0]]
                puzzle[swap[0]]=puzzle[swap[1]]
                puzzle[swap[1]]=temp
                
            elif roworcolumn==2: # i.e. swap columns
                for j in range(9):
                    temp=puzzle[j][swap[0]]
                    puzzle[j][swap[0]]=puzzle[j][swap[1]]
                    puzzle[j][swap[1]]=temp


        #for row in puzzle:
            #print(row)
        #print("\n")
                    

    removex=random.randint(0,8)
    removey=random.randint(0,8)

    while puzzle[removex][removey]=="_":

        removex=random.randint(0,8)
        removey=random.randint(0,8)

    removed.append([removex,removey,puzzle[removex][removey],0]) # x and y coords of cell, value that cell held, number of attempts to remove another cell after
    puzzle[removex][removey]="_"

    #for row in puzzle:
        #print(row)
    #print("\n")

    if len(removed)>1:
        
        removed[-2][3]+=1

    aipuzzle=copy.deepcopy(puzzle)
    ai=SudokuAI(aipuzzle)
    solved=ai.solvePuzzle(difficulty)
    

    if len(solved)!=3: # no solution returned

        for i in range(15):

            add=removed.pop(-1)
            puzzle[add[0]][add[1]]=add[2]

        removed[-1][3]+=1

        deadends+=1

        if deadends<5:
            
            return generatePuzzle(difficulty,puzzle,removed,removecount,start,deadends)

        else:

            return generatePuzzle(difficulty,[],[],0,time.time(),0)
    

    elif solved[2]!=True or (difficulty=="easy" and len(removed)<removecount): # solution returned but inadequate difficulty puzzle

        return generatePuzzle(difficulty,puzzle,removed,removecount,start,deadends)
    

    elif solved[2]==True and (difficulty!="easy" or len(removed)<removecount+6): # solution returned and adequate difficulty

        return (puzzle,solved[0])
    

    """else:

        for i in range(15):

            add=removed.pop(-1)
            puzzle[add[0]][add[1]]=add[2]

        removed[-1][3]+=1

        return generatePuzzle(difficulty,puzzle,removed,removecount,start)"""


    
        


"""def generatePuzzle(difficulty,puzzle=[],remove=0,previoussolution=[],difficultymet=False):

    if puzzle==[]: # this runs only on first call to generate the full puzzle

        if difficulty=="dev":
            remove=1
        elif difficulty=="easy":
            remove=random.randint(37,43)
        elif difficulty=="medium":
            remove=random.randint(45,50)
        else:
            remove=random.randint(55,61) # remove i.e. number of values that will be removed (number of recursions)

        row=["1","2","3","4","5","6","7","8","9"] # generate valid puzzle using circular shifts
        random.shuffle(row)
        for i in range(3):
            row=circularShift(row,1)
            puzzle.append(row)
            row=circularShift(row,3)
            puzzle.append(row)
            row=circularShift(row,3)
            puzzle.append(row)

        swaps=((0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(6,7),(6,8),(7,8)) # rows/columns that can be swapped whilst staying valid
        for i in range(150): # randomly swap rows/columns to get rid of shift pattern
            roworcolumn=random.randint(1,2)
            swap=swaps[random.randint(0,len(swaps)-1)]
            
            if roworcolumn==1: # i.e. swap rows
                temp=puzzle[swap[0]]
                puzzle[swap[0]]=puzzle[swap[1]]
                puzzle[swap[1]]=temp
                
            elif roworcolumn==2: # i.e. swap columns
                for j in range(9):
                    temp=puzzle[j][swap[0]]
                    puzzle[j][swap[0]]=puzzle[j][swap[1]]
                    puzzle[j][swap[1]]=temp

    selection=random.randint(1,10)
    

    if selection in range(1,3) and difficulty=="hard": # remove arrangement of cells that enables hard techniques
                                                        # selection=1 or 2: x/xy wing, 3: swordfish
        if selection==1:
            selection=2
            
        digit=str(random.randint(1,9))
        removerows=[]
        removecolumns=[]
        
        for row in range(len(puzzle)):

            for column in range(len(puzzle[row])):

                if puzzle[row][column]==digit:

                    removerows.append(row)
                    removecolumns.append(column)
                    
                    if len(removerows)>=selection:
                        
                        break

            if len(removerows)>=selection:

                break

        for row in removerows:

            for column in removecolumns:

                if (len(removerows)==3 and random.randint(1,20) in range(1,15)) or len(removerows)==2:

                    puzzle[row][column]="_"


    elif (selection in range(1,4) and difficulty=="medium") or (selection==4 and difficulty=="hard"): # remove arrangements that allow for triples and quads

        selection2=random.randint(1,3)
        removecells=random.randint(3,4)
        removeposition=random.randint(1,9)
        if selection2==3:
            removeblock=(random.randint(0,2),random.randint(0,2))

        while removecells>0:

            x=random.randint(0,8)
            y=random.randint(0,8)

            if selection2==1 and removeposition==x:

                puzzle[x][y]="_"
                removecells-=1

            elif selection2==2 and removeposition==y:

                puzzle[x][y]="_"
                removecells-=1

            elif selection2==3 and (x//3,y//3)==removeblock:

                puzzle[x][y]="_"
                removecells-=1
        

    else:                    

        while True: # remove a single random value that is not already empty, keep track of value in case unsolvable

            x=random.randint(0,8)
            y=random.randint(0,8)
            if puzzle[x][y]!="_":
                tempstore=puzzle[x][y]
                puzzle[x][y]="_"
                break


    aipuzzle=copy.deepcopy(puzzle)
    ai=SudokuAI(aipuzzle)
    solved=ai.solvePuzzle(difficulty)
    
    if len(solved)!=3: # returns no solution = AI cannot solve it, stop removing cells

        #puzzle[x][y]=tempstore
        aipuzzle=copy.deepcopy(previoussolution)
        ai=SudokuAI(aipuzzle)
        solved=ai.solvePuzzle(difficulty)

        if difficultymet==True:
            
            return (previoussolution,solved[0])

        else:

            return None

    elif solved[2]==True:

        difficultymet=True

        if difficulty=="medium" or difficulty=="hard":

            return (puzzle,solved[0])
    
    elif remove==0: # specified limit reached, stop removing cells

        if difficultymet==True:
        
            return (puzzle,solved[0])

        else:

            return None
    
    else: # continue removing cells
        
        previoussolution=copy.deepcopy(puzzle)
        return generatePuzzle(difficulty,puzzle,remove-1,previoussolution,difficultymet)"""
        

"""valuedcells=[]
    for i in range(9):
        for j in range(9):
            valuedcells.append((i,j))
    for i in range(remove): # remove values from random cells
        remove=valuedcells.pop(random.randint(0,len(valuedcells)-1))
        puzzle[remove[0]][remove[1]]="_"

    aipuzzle=copy.deepcopy(puzzle)
    ai=SudokuAI(aipuzzle)
    solved=ai.solvePuzzle()
    if len(solved)==2: # i.e. AI could solve it (returns a solution)
        return (puzzle,solved[0])
    else:
        return generatePuzzle(difficulty,recursionCount+1)"""
