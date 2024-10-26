import random
import copy


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



difficulty="hard"
puzzle=generatePuzzle(difficulty)
for row in puzzle[0]:
    print(row)
print("\n")
for row in puzzle[1]:
    print(row)
print("\n")
