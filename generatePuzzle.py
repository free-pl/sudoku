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
