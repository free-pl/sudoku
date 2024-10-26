from knowledge import *
from ai import *
import random
import copy
import pygame
import time



def generatePuzzle(difficulty):

    puzzlebank=open(f"puzzlebank{difficulty}.txt","r")
    templates=puzzlebank.read()
    templates=templates.split("\n")
    puzzlebank.close()
    del templates[-1]
    selection=random.randint(0,len(templates)-1)

    for i in range(len(templates)): # choose a random template

        if i==selection:
            
            template=templates[i].split(",")
            break

    puzzlestr=template[0]
    solutionstr=template[1]
    puzzle=[[],[],[],[],[],[],[],[],[]]
    solution=[[],[],[],[],[],[],[],[],[]]



    digits=["1","2","3","4","5","6","7","8","9"] # assign random digits
    random.shuffle(digits)
    assignment={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8}

    for char in range(len(solutionstr)):

        temp=digits[assignment[solutionstr[char]]]

        if puzzlestr[char]!="_":

            puzzle[char//9].append(temp) # adding chars into 2d lists

        else:

            puzzle[char//9].append("_")
            
        solution[char//9].append(temp)



    rotations=random.randint(0,3) # rotate the puzzle anticlockwise random number of times using 2 reflections

    for i in range(rotations):

        rotatedpuzzle=copy.deepcopy(puzzle)
        rotatedsolution=copy.deepcopy(solution)

        for row in range(len(puzzle)):

            for column in range(len(puzzle[row])):

                rotatedpuzzle[column][row]=puzzle[row][column]
                rotatedsolution[column][row]=solution[row][column]

        rotatedpuzzle.reverse()
        rotatedsolution.reverse()
        puzzle=copy.deepcopy(rotatedpuzzle)
        solution=copy.deepcopy(rotatedsolution)



    shiftsvertical=random.randint(0,2) # shift blocks vertically 0-2 times

    for i in range(shiftsvertical*3):

        moverow=puzzle.pop(0)
        puzzle.append(moverow)
        moverow=solution.pop(0)
        solution.append(moverow)



    shiftshorizontal=random.randint(0,2) # shift blocks horizontally 0-2 times

    for i in range(shiftshorizontal*3):

        for row in range(len(puzzle)):

            shiftcell=puzzle[row].pop(0)
            puzzle[row].append(shiftcell)
            shiftcell=solution[row].pop(0)
            solution[row].append(shiftcell)



    mirrored=random.choice([True,False]) # mirror the puzzle or leave unchanged

    if mirrored==True:

        puzzle.reverse()
        solution.reverse()



    return (puzzle,solution)


        
def checkCompletion(puzzle):

    for row in puzzle:
        for cell in row:
            if cell=="_":
                return False
    return True



def checkValidity(puzzle):

    rows=puzzle # the puzzle is already represented as rows so no need to do extra here, top to bottom
    columns=[[],[],[],[],[],[],[],[],[]] # left to right
    blocks=[[],[],[],[],[],[],[],[],[]] # each 3x3 block, left to right then top to bottom, contents of each block read the same way

    blockvalues=((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)) # find which block to add a cell to by taking row and column from below and floor dividing by 3 to convert into one of these coordinates for blocks

    for row in range(len(puzzle)): # nested loop rearranges puzzle into columns and blocks
        for column in range(len(puzzle[row])):
            columns[column].append(puzzle[row][column])
            block=(row//3,column//3)
            for coord in range(len(blockvalues)):
                if block==blockvalues[coord]:
                    blocks[coord].append(puzzle[row][column])
                    break
            continue
    del block # to reuse name in later loop :)

    for row in rows: # check for no repeating digits
        counts={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
        for cell in row:
            try:
                counts[cell]+=1 # no need to keep count of "_" hence try except
            except:
                pass
        for count in counts:
            if counts[count]>1:
                return False

    for column in columns:
        counts={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
        for cell in column:
            try:
                counts[cell]+=1 
            except:
                pass
        for count in counts:
            if counts[count]>1:
                return False

    for block in blocks: 
        counts={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
        for cell in block:
            try:
                counts[cell]+=1 
            except:
                pass
        for count in counts:
            if counts[count]>1:
                return False

    return True
