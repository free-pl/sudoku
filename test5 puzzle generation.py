import time
#import multiprocessing
from ai import *
from game import *
from knowledge import *



def numbersToLetters(puzzle): # switch numbers to letters, later the letters can be assigned random nubmbers for more variety
    indextoletter=["_","a","b","c","d","e","f","g","h","i"]
    string=""
    for i in puzzle:
        for j in i:
            if j!="_":
                j=indextoletter[int(j)]
            string+=j
    return string




difficulty="hard"

starttime=time.time()

attempts=0

for i in range(333):

    puzzle=None

    while puzzle==None:

        try:

            puzzle=generatePuzzle(difficulty,[],[],0,time.time(),0)

            if puzzle!=None:

                puzzlebank=open(f"puzzlebank{difficulty}.txt","a")
                initial=numbersToLetters(puzzle[0])
                solution=numbersToLetters(puzzle[1])
                puzzlebank.write(f"{initial},{solution}\n")
                attempts+=1
                print(f"Generated puzzle {attempts} after {int(time.time()-starttime)}s")
                puzzlebank.close()

        except:

            continue

    

print(f"Time taken to generate: {int(time.time()-starttime)}s")

"""initialpuzzle=puzzle[0]
solution=puzzle[1]

for row in initialpuzzle:

    print(row)

print("\n")

for row in solution:

    print(row)"""
