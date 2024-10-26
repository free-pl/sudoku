class Knowledge: # represents individual knowledge i.e. for one cell in the puzzle

    def __init__(self,row,column):
        
        self.__row=row
        self.__column=column
        self.__block=-1 # assigned in Puzzle init() method
        self.__candidates=set() # initial candidates calculated in Puzzle class when that is initialised



    def __eq__(self,cell2):

        if isinstance(cell2,Knowledge):

            if self.__row==cell2.getRow() and self.__column==cell2.getColumn():

                return True

        return False



    def getRow(self):
        
        return self.__row



    def getColumn(self):
        
        return self.__column



    def getCandidates(self):
        
        return self.__candidates



    def getBlock(self):

        return self.__block



    def setBlock(self,block):

        self.__block=block



    def showKnowledge(self):

        return f"({self.__row},{self.__column}), block {self.__block}, candidates: {self.__candidates}"



    def setCandidates(self,candidates):
        
        self.__candidates=candidates



    def removeCandidates(self,remove): # remove is a set of candidates to be removed from the list
        
        self.__candidates=self.__candidates.difference(remove)



class Puzzle: # represents an entire sudoku puzzle

    def __init__(self,puzzle): # puzzle is the whole puzzle in the form of a 2D array, but will be stored as rows/columns/blocks for the AI to use
        
        self.__knowledge=[]
        self.__rows=puzzle # the puzzle is already represented as rows so no need to do extra here, top to bottom
        self.__columns=[[],[],[],[],[],[],[],[],[]] # left to right
        self.__blocks=[[],[],[],[],[],[],[],[],[]] # each 3x3 block, left to right then top to bottom, contents of each block read the same way

        self.__blockvalues=((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)) # find which block to add a cell to by taking row and column from below and floor dividing by 3 to convert into one of these coordinates for blocks

        for row in range(len(puzzle)): # nested loop rearranges puzzle into columns and blocks
            for column in range(len(puzzle[row])):
                self.__columns[column].append(puzzle[row][column])
                block=(row//3,column//3)
                for coord in range(len(self.__blockvalues)):
                    if block==self.__blockvalues[coord]:
                        self.__blocks[coord].append(puzzle[row][column])
                        break
                continue

        for row in range(len(puzzle)): # another nested loop for calculating candidates to create the initial knowledge base
            for column in range(len(puzzle)):
                if puzzle[row][column]=="_":
                    self.__knowledge.append(Knowledge(row,column))
                    candidates=set(["1","2","3","4","5","6","7","8","9"])
                    candidates=candidates.difference(set(self.__rows[row]))
                    candidates=candidates.difference(set(self.__columns[column]))
                    block=(row//3,column//3)
                    for coord in range(len(self.__blockvalues)):
                        if block==self.__blockvalues[coord]:
                            self.__knowledge[-1].setBlock(coord)
                            candidates=candidates.difference(set(self.__blocks[coord]))
                            break
                    self.__knowledge[-1].setCandidates(candidates) # using set difference functions to work out digits which do not clash with what is already in the puzzle
                continue



    def getKnowledge(self):

        return self.__knowledge



    def getRows(self):

        return self.__rows



    def getColumns(self):

        return self.__columns



    def getBlocks(self):

        return self.__blocks



    def showKnowledge(self): # just for testing purposes

        for i in self.__knowledge:
            print(i.showKnowledge())



    def updateKnowledge(self,remove,row,column): # remove variable represents candidates to be removed from cell
        
        for knowledge in self.__knowledge: # find cell in knowledge base
            if row==knowledge.getRow() and column==knowledge.getColumn():
                knowledge.removeCandidates(remove)
                break



    def addValue(self,value,row,column):

        self.__rows[row][column]=value # update value in row, column, and block
        self.__columns[column][row]=value
        block=(row//3,column//3)
        for coord in range(len(self.__blockvalues)):
            if block==self.__blockvalues[coord]:
                position=(row%3)*3+(column%3) # find position of desired cell within its block by doing this calculation
                self.__blocks[coord][position]=value
                break
        for cell in self.__knowledge: # delete that cell from knowledge base now that we know the value
            if cell.getRow()==row and cell.getColumn()==column:
                self.__knowledge.remove(cell)
                break
        value=set(value) # now remove the candidate from intersecting cells
        for cell in self.__knowledge:
            if cell.getRow()==row or cell.getColumn()==column or cell.getBlock()==block:
                self.updateKnowledge(value,cell.getRow(),cell.getColumn())
