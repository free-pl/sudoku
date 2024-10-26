from knowledge import *
from ai import *
import random
import copy
import multiprocessing
import time



def circularShift(array,shift):

    array2=copy.copy(array)
    for i in range(shift):
        value=array2[0]
        del array2[0]
        array2.append(value)
    return array2



def generatePuzzle(difficulty):

    if difficulty=="dev":
        remove=1
    elif difficulty=="easy":
        remove=random.randint(37,43)
    elif difficulty=="medium":
        remove=random.randint(43,48)
    else:
        remove=random.randint(49,51) # remove i.e. number of values that will be removed

    puzzle=[]

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

    valuedcells=[]
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
        return None



def numbersToLetters(puzzle): # switch numbers to letters, later the letters can be assigned random nubmbers for more variety
    indextoletter=["null","a","b","c","d","e","f","g","h","i"]
    string=""
    for i in puzzle:
        for j in i:
            if j!="_":
                j=indextoletter[int(j)]
            string+=j
    return string



def findPuzzles():

    puzzlebank=open("puzzlebankhard.txt","a")
    count=0

    while count<=16666:
        difficulty="hard"
        generated=generatePuzzle(difficulty)
        if generated==None:
            continue

        puzzle=numbersToLetters(generated[0])
        solution=numbersToLetters(generated[1])
        string=puzzle+","+solution+"\n"
        puzzlebank.write(string)
        count+=1

    puzzlebank.close()

    print("loop finished")



if __name__=="__main__":


    loop1=multiprocessing.Process(target=findPuzzles)
    loop2=multiprocessing.Process(target=findPuzzles)
    loop3=multiprocessing.Process(target=findPuzzles)
    loop4=multiprocessing.Process(target=findPuzzles)
    loop5=multiprocessing.Process(target=findPuzzles)
    loop6=multiprocessing.Process(target=findPuzzles)
    
    start=time.time()
    
    loop1.start()
    loop2.start()
    loop3.start()
    loop4.start()
    loop5.start()
    loop6.start()

    loop1.join()
    loop2.join()
    loop3.join()
    loop4.join()
    loop5.join()
    loop6.join()
    
    end=time.time()
    print(end-start)


    
