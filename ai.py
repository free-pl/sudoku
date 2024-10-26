from knowledge import *
import time
import copy

class SudokuAI: # contains the AI for solving a given puzzle arrangement

    def __init__(self,puzzle):

        self.__puzzle=Puzzle(puzzle)
        self.__resolved=[] # contains pairs/triples/quads already resolved to avoid them



    def getPuzzle(self):

        return self.__puzzle



    def nakedSingle(self): # search for a cell with only one candidate

        for cell in self.__puzzle.getKnowledge(): # simple loop to find cell with one candidate
            
            candidates=tuple(cell.getCandidates())
            
            if len(candidates)==1:
                
                for value in candidates:
                    
                    row=cell.getRow()
                    column=cell.getColumn()
                    block=cell.getBlock()
                    self.__puzzle.addValue(value,row,column)
                    
                    return [{(row,column)},set(candidates)] # all methods return in format of involved coords and candidates



    def hiddenSingle(self): # search for a cell with a candidate that has no intersecting instances

        for cell in self.__puzzle.getKnowledge(): # get candidates etc of first cell
            
            candidatesRow=cell.getCandidates()
            candidatesColumn=cell.getCandidates()
            candidatesBlock=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()
            
            for cell2 in self.__puzzle.getKnowledge(): # compare first cell to rest of row/column/block
                
                if cell2!=cell: # separate candidate sets for intersecting row, column & block
                    
                    if cell2.getRow()==row:
                        
                        candidates2=cell2.getCandidates()
                        candidatesRow=candidatesRow.difference(candidates2)
                        
                    elif cell2.getColumn==column:
                        
                        candidates2=cell2.getCandidates()
                        candidatesColumn=candidatesColumn.difference(candidates2)
                        
                    elif cell2.getBlock==block:
                        
                        candidates2=cell2.getCandidates()
                        candidatesBlock=candidatesBlock.difference(candidates2)
                        
            if len(candidatesRow)==1: # add value to the puzzle if hidden single found
                
                candidates=tuple(candidatesRow)
                self.__puzzle.addValue(candidates[0],row,column)
                
                return [{(row,column)},set(candidates)]
            
            elif len(candidatesColumn)==1:
                
                candidates=tuple(candidatesColumn)
                self.__puzzle.addValue(candidates[0],row,column)
                
                return [{(row,column)},set(candidates)]
            
            elif len(candidatesBlock)==1:
                
                candidates=tuple(candidatesBlock)
                self.__puzzle.addValue(candidates[0],row,column)
                
                return [{(row,column)},set(candidates)]



    def nakedPair(self): # search for two intersecting cells with only the two same candidates to eliminate candidates

        for cell in self.__puzzle.getKnowledge(): # get candidates etc of first cell
            
            candidates=cell.getCandidates()
            
            if len(candidates)==2:
                
                row=cell.getRow()
                column=cell.getColumn()
                block=cell.getBlock()
                
                for cell2 in self.__puzzle.getKnowledge(): # if first cell has 2 candidates then compare to second
                    
                    if cell2.getCandidates()==candidates and cell2!=cell:

                        changemade=False
                        
                        if cell2.getRow()==row and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here remove candidates from rest of row
                            
                            for cell3 in self.__puzzle.getKnowledge():
                                
                                if cell3.getRow()==row and cell3!=cell2 and cell3!=cell:

                                    oldcandidates=cell3.getCandidates()
                                    column3=cell3.getColumn()
                                    self.__puzzle.updateKnowledge(candidates,row,column3)
                                    newcandidates=cell3.getCandidates()

                                    if oldcandidates!=newcandidates:

                                        changemade=True
                                    
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(row,cell2.getColumn())},candidates]
                        
                        
                        elif cell2.getColumn()==column and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here remove candidates from rest of column
                            
                            for cell3 in self.__puzzle.getKnowledge():
                                
                                if cell3.getColumn()==column and cell3!=cell2 and cell3!=cell:
                                    
                                    oldcandidates=cell3.getCandidates()
                                    row3=cell3.getRow()
                                    self.__puzzle.updateKnowledge(candidates,row3,column)
                                    newcandidates=cell3.getCandidates()

                                    if oldcandidates!=newcandidates:

                                        changemade=True
                                    
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(cell2.getRow(),column)},candidates]
                        
                        
                        elif cell2.getBlock()==block and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here remove candidates from rest of block
                            
                            for cell3 in self.__puzzle.getKnowledge():
                                
                                if cell3.getBlock()==block and cell3!=cell2 and cell3!=cell:

                                    oldcandidates=cell3.getCandidates()
                                    row3=cell3.getRow()
                                    column3=cell3.getColumn()
                                    self.__puzzle.updateKnowledge(candidates,row3,column3)
                                    newcandidates=cell3.getCandidates()

                                    if oldcandidates!=newcandidates:

                                        changemade=True
                                    
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(cell2.getRow(),cell2.getColumn())},candidates]



    def hiddenPair(self): # search for two intersecting cells including the two same candidates to eliminate others from those cells

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()
            
            for cell2 in self.__puzzle.getKnowledge():
                
                candidates2=cell2.getCandidates()
                intersect=candidates.intersection(candidates2)
                
                if len(intersect)>=2 and cell2!=cell:

                    changemade=False
                    
                    if cell2.getRow()==row and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here compare candidates from rest of row
                        
                        for cell3 in self.__puzzle.getKnowledge():
                            
                            if cell3.getRow()==row and cell3!=cell2 and cell3!=cell:
                                
                                intersect=intersect.difference(cell3.getCandidates())
                                
                        if len(intersect)==2: # if there are exactly two candidates which only exist in cell and cell2
                            
                            changemade=True
                            cell.setCandidates(intersect)
                            cell2.setCandidates(intersect)
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(row,cell2.getColumn())},intersect]

                        
                    elif cell2.getColumn()==column and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here compare candidates from rest of column
                        
                        for cell3 in self.__puzzle.getKnowledge():
                            
                            if cell3.getColumn()==column and cell3!=cell2 and cell3!=cell:
                                
                                intersect=intersect.difference(cell3.getCandidates())
                                
                        if len(intersect)==2:
                            
                            changemade=True
                            cell.setCandidates(intersect)
                            cell2.setCandidates(intersect)
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(cell2.getRow(),column)},intersect]

                        
                    elif cell2.getBlock()==block and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved: # here compare candidates from rest of block
                        
                        for cell3 in self.__puzzle.getKnowledge():
                            
                            if cell3.getBlock()==block and cell3!=cell2 and cell3!=cell:
                                
                                intersect=intersect.difference(cell3.getCandidates())
                                
                        if len(intersect)==2:

                            changemade=True
                            cell.setCandidates(intersect)
                            cell2.setCandidates(intersect)
                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:
                            
                                return [{(row,column),(cell2.getRow(),cell2.getColumn())},intersect]


                    
    def pointingPairOrTriple(self): # search for a candidate which appears only twice/thrice in a block but also in the same row/column

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()
            
            for cell2 in self.__puzzle.getKnowledge():
                
                if cell2!=cell and cell2.getBlock()==block and (cell2.getRow()==row or cell2.getColumn()==column) and {(row,column),(cell2.getRow(),cell2.getColumn())} not in self.__resolved:

                    if cell2.getRow()==row:

                        sameRow=True

                    else:

                        sameRow=False # false because they are in the same column instead

                    candidates2=cell2.getCandidates()
                    intersect=candidates.intersection(candidates2)
                    
                    for cell3 in self.__puzzle.getKnowledge(): # find candidates also present elsewhere in the block to ignore

                        if cell3.getBlock()==block and cell3!=cell2 and cell3!=cell:

                            if (sameRow==True and cell3.getRow()!=row) or (sameRow==False and cell3.getColumn()!=column):

                                intersect=intersect.difference(cell3.getCandidates()) # ignore third cell in same row/column in case there is a triple
                                
                    if len(intersect)==1: # if there is a pointing pair then remove that candidate from rest of row/column

                        changemade=False

                        if cell2.getRow()==row:

                            for cell3 in self.__puzzle.getKnowledge():

                                if cell3.getRow()==row and cell3.getBlock()!=block:

                                    oldcandidates=cell3.getCandidates()
                                    self.__puzzle.updateKnowledge(intersect,row,cell3.getColumn())
                                    newcandidates=cell3.getCandidates()

                                    if oldcandidates!=newcandidates:

                                        changemade=True

                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:

                                return [{(row,column),(row,cell2.getColumn())},intersect]

                        elif cell2.getColumn()==column:

                            for cell3 in self.__puzzle.getKnowledge():

                                if cell3.getColumn()==column and cell3.getBlock()!=block:

                                    oldcandidates=cell3.getCandidates()
                                    self.__puzzle.updateKnowledge(intersect,cell3.getRow(),column)
                                    newcandidates=cell3.getCandidates()

                                    if oldcandidates!=newcandidates:

                                        changemade=True

                            self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn())})

                            if changemade==True:

                                return [{(row,column),(cell2.getRow(),column)},intersect]


                
    def nakedOrHiddenTriple(self): # search for three intersecting cells with some exclusive combination of three candidates to then eliminate them from other cells

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()
            
            for cell2 in self.__puzzle.getKnowledge():
                
                if cell2!=cell and (cell2.getBlock()==block or cell2.getRow()==row or cell2.getColumn()==column):
                    
                    if cell2.getRow()==row:
                        
                        sameRow=True
                        
                    elif cell2.getColumn()==column:
                        
                        sameRow=False # false i.e. same column instead
                        
                    else:
                        
                        sameRow=None # none i.e. same block instead
                        
                    union=candidates.union(cell2.getCandidates())
                    
                    for cell3 in self.__puzzle.getKnowledge(): # compare first two cells to third
                        
                        if cell3!=cell2 and cell3!=cell and {(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn())} not in self.__resolved:
                            
                            if (sameRow==True and cell3.getRow()==row) or (sameRow==False and cell3.getColumn()==column) or (sameRow==None and cell3.getBlock()==block):
                                
                                union2=union.union(cell3.getCandidates())
                                
                                if len(union2)>3: # in this case compare against other intersecting cells to check for hidden triple
                                    
                                    for cell4 in self.__puzzle.getKnowledge():
                                        
                                        if (sameRow==True and cell4.getRow()==row) or (sameRow==False and cell4.getColumn()==column) or (sameRow==None and cell4.getBlock()==block):
                                            
                                            if cell4!=cell3 and cell4!=cell2 and cell4!=cell:
                                                
                                                union2=union2.difference(cell4.getCandidates())
                                                
                                if len(union2)==3: # if the three cells together share some combination of three candidates

                                    changemade=False
                                    
                                    for cell4 in self.__puzzle.getKnowledge():
                                        
                                        if (sameRow==True and cell4.getRow()==row) or (sameRow==False and cell4.getColumn()==column) or (sameRow==None and cell4.getBlock()==block):
                                            
                                            if cell4!=cell3 and cell4!=cell2 and cell4!=cell:

                                                oldcandidates=cell4.getCandidates()
                                                self.__puzzle.updateKnowledge(union2,cell4.getRow(),cell4.getColumn())
                                                newcandidates=cell4.getCandidates()

                                                if oldcandidates!=newcandidates:

                                                    changemade=True

                                                
                                    self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn())})

                                    if changemade==True:
                                        
                                        return [{(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn())},union2]


                    
    def nakedOrHiddenQuad(self): # search for four intersecting cells with some exclusive combination of four candidates to then eliminate them from other cells

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()
            
            for cell2 in self.__puzzle.getKnowledge():
                
                if cell2!=cell and (cell2.getBlock()==block or cell2.getRow()==row or cell2.getColumn()==column):
                    
                    if cell2.getRow()==row:
                        
                        sameRow=True
                        
                    elif cell2.getColumn()==column:
                        
                        sameRow=False # false i.e. same column instead
                        
                    else:
                        
                        sameRow=None # none i.e. same block instead
                        
                    union=candidates.union(cell2.getCandidates())
                    
                    for cell3 in self.__puzzle.getKnowledge():
                        
                        if cell3!=cell2 and cell3!=cell:
                            
                            if (sameRow==True and cell3.getRow()==row) or (sameRow==False and cell3.getColumn()==column) or (sameRow==None and cell3.getBlock()==block):
                                
                                union2=union.union(cell3.getCandidates())
                                
                                for cell4 in self.__puzzle.getKnowledge(): # compare fourth cell to first three
                                    
                                    if cell4!=cell3 and cell4!=cell2 and cell4!=cell and {(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn()),(cell4.getRow(),cell4.getColumn())} not in self.__resolved:

                                        if (sameRow==True and cell4.getRow()==row) or (sameRow==False and cell4.getColumn()==column) or (sameRow==None and cell4.getBlock()==block):

                                            union3=union2.union(cell4.getCandidates())
                                            
                                            if len(union3)>4: # in this case compare against other intersecting cells to check for hidden quad

                                                for cell5 in self.__puzzle.getKnowledge():

                                                    if (sameRow==True and cell5.getRow()==row) or (sameRow==False and cell5.getColumn()==column) or (sameRow==None and cell5.getBlock()==block):

                                                        if cell5!=cell4 and cell5!=cell3 and cell5!=cell2 and cell5!=cell:

                                                            union3=union3.difference(cell5.getCandidates())

                                            if len(union3)==4: # if the four cells together share some combination of four candidates

                                                changemade=False

                                                for cell5 in self.__puzzle.getKnowledge():

                                                    if (sameRow==True and cell5.getRow()==row) or (sameRow==False and cell5.getColumn()==column) or (sameRow==None and cell5.getBlock()==block):

                                                        if cell5!=cell4 and cell5!=cell3 and cell5!=cell2 and cell5!=cell:

                                                            oldcandidates=cell5.getCandidates()
                                                            self.__puzzle.updateKnowledge(union3,cell5.getRow(),cell5.getColumn())
                                                            newcandidates=cell5.getCandidates()

                                                            if oldcandidates!=newcandidates:

                                                                changemade=True

                                                self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn()),(cell4.getRow(),cell4.getColumn())})

                                                if changemade==True:

                                                    return [{(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn()),(cell4.getRow(),cell4.getColumn())},union3]



    def xWing(self):

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()

            for cell2 in self.__puzzle.getKnowledge(): # test for x wing on two cells in same row
                
                candidates2=cell2.getCandidates()
                row2=cell2.getRow()
                column2=cell2.getColumn()
                block2=cell2.getBlock()

                if column2!=column and row2==row:

                    for cell3 in self.__puzzle.getKnowledge():
                        
                        candidates3=cell3.getCandidates()
                        row3=cell3.getRow()
                        column3=cell3.getColumn()
                        block3=cell3.getBlock()

                        for cell4 in self.__puzzle.getKnowledge(): # check aligning 2 cells in preceding rows
                            
                            candidates4=cell4.getCandidates()
                            row4=cell4.getRow()
                            column4=cell4.getColumn() # below if statement tests that they make the rectangle shape we want
                            block4=cell4.getBlock()

                            if row4==row3 and row4!=row2 and column3==column and column4==column2 and {(row,column),(row2,column2),(row3,column3),(row4,column4)} not in self.__resolved:

                                if block4==block3 and block4==block2 and block4==block: # exclude case where all 4 cells in same block
                                    
                                    break

                                sharedcandidate=candidates.intersection(candidates2,candidates3,candidates4)

                                if len(sharedcandidate)==1: # check that they share a common candidate for the x wing

                                    presentinrow=False
                                    presentincolumn=False

                                    for cell5 in self.__puzzle.getKnowledge(): # checking that that candidate is also present in EITHER row or column (xor)
                                        
                                        candidates5=cell5.getCandidates()
                                        row5=cell5.getRow()
                                        column5=cell5.getColumn()
                                        
                                        if len(candidates5.intersection(sharedcandidate))==1 and cell5!=cell4 and cell5!=cell3 and cell5!=cell2 and cell5!=cell:

                                            if row5==row3 or row5==row:
                                                
                                                presentinrow=True

                                            if column5==column2 or column5==column:
                                                
                                                presentincolumn=True

                                    if presentinrow!=presentincolumn: # xor statement

                                        changemade=False

                                        for cell5 in self.__puzzle.getKnowledge(): # finally updates other candidates if x wing conditions satisfied
                                            
                                            row5=cell5.getRow()
                                            column5=cell5.getColumn()

                                            if cell5!=cell4 and cell5!=cell3 and cell5!=cell2 and cell5!=cell:

                                                if (presentinrow==True and (row5==row or row5==row3)) or (presentincolumn==True and (column5==column or column5==column2)):

                                                    oldcandidates=cell5.getCandidates()
                                                    self.__puzzle.updateKnowledge(sharedcandidate,row5,column5)
                                                    newcandidates=cell5.getCandidates()

                                                    if oldcandidates!=newcandidates:

                                                        changemade=True

                                        self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn()),(cell4.getRow(),cell4.getColumn())})
                                        
                                        if changemade==True:

                                            return [{(row,column),(row2,column2),(row3,column3),(row4,column4)},sharedcandidate]



    def xyWing(self):

        for cell in self.__puzzle.getKnowledge():
            
            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()

            for cell2 in self.__puzzle.getKnowledge():
                
                candidates2=cell2.getCandidates()
                row2=cell2.getRow()
                column2=cell2.getColumn()
                block2=cell2.getBlock()
                                                                            # if the two cells do not intersect, share 1 candidate, and each have 2 candidates
                sharedcandidates=candidates.intersection(candidates2)
                
                if row!=row2 and column!=column2 and block!=block2 and len(sharedcandidates)==1 and len(candidates)==2 and len(candidates2)==2:

                    for cell3 in self.__puzzle.getKnowledge():
                        
                        candidates3=cell3.getCandidates()
                        row3=cell3.getRow()
                        column3=cell3.getColumn()
                        block3=cell3.getBlock()     # below describes when xy wing conditions are met
                                                # if the third cell intersects both other cells and has 2 candidates, both of which are in the other cells but not the same shared one
                        if (row3==row2 or column3==column2 or block3==block2) and cell3!=cell2 and (row3==row or column3==column or block3==block) and cell3!=cell and {(row,column),(row2,column2),(row3,column3)} not in self.__resolved:

                            if len(sharedcandidates.intersection(candidates3))==0 and len(candidates3.intersection(candidates2))==1 and len(candidates3.intersection(candidates))==1 and len(candidates3)==2:

                                for cell4 in self.__puzzle.getKnowledge():
                                    
                                    row4=cell4.getRow()
                                    column4=cell4.getColumn()
                                    block4=cell4.getBlock()

                                    if ((row4==row2 or column4==column2 or block4==block2) and cell4!=cell2) and ((row4==row or column4==column or block4==block) and cell4!=cell):

                                        self.__puzzle.updateKnowledge(sharedcandidates,row4,column4)

                                self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn())})

                                return [{(row,column),(row2,column2),(row3,column3)},sharedcandidates] # below is xyz-wing which is an extension/special case of xy-wing

                            elif len(sharedcandidates.intersection(candidates3))==1 and len(candidates3.intersection(candidates2))==2 and len(candidates3.intersection(candidates))==2 and len(candidates3)==3:

                                changemade=False

                                for cell4 in self.__puzzle.getKnowledge():

                                    row4=cell4.getRow()
                                    column4=cell4.getColumn()
                                    block4=cell4.getBlock()

                                    if ((row4==row3 or column4==column3 or block4==block3) and cell4!=cell3) and ((row4==row2 or column4==column2 or block4==block2) and cell4!=cell2) and ((row4==row or column4==column or block4==block) and cell4!=cell):

                                        oldcandidates=cell4.getCandidates()
                                        self.__puzzle.updateKnowledge(sharedcandidates,row4,column4)
                                        newcandidates=cell4.getCandidates()

                                        if oldcandidates!=newcandidates:

                                            changemade=True

                                self.__resolved.append({(row,column),(cell2.getRow(),cell2.getColumn()),(cell3.getRow(),cell3.getColumn())})

                                if changemade==True:

                                    return [{(row,column),(row2,column2),(row3,column3)},sharedcandidates]



    def swordfish(self):

        for cell in self.__puzzle.getKnowledge():

            candidates=cell.getCandidates()
            row=cell.getRow()
            column=cell.getColumn()
            block=cell.getBlock()

            for cell2 in self.__puzzle.getKnowledge():

                candidates2=cell2.getCandidates()
                row2=cell2.getRow()
                column2=cell2.getColumn()
                block2=cell2.getBlock()

                sharedcandidates=candidates.intersection(candidates2)

                if row2==row and cell2!=cell and len(sharedcandidates)>0:

                    tempcandidates=sharedcandidates

                    for cell3 in self.__puzzle.getKnowledge():

                        candidates3=cell3.getCandidates()
                        row3=cell3.getRow()
                        column3=cell3.getColumn()
                        block3=cell3.getBlock()

                        sharedcandidates=tempcandidates.intersection(candidates3)

                        if row3!=row and len(sharedcandidates)>0:

                            tempcandidates=sharedcandidates

                            for cell4 in self.__puzzle.getKnowledge():

                                candidates4=cell4.getCandidates()
                                row4=cell4.getRow()
                                column4=cell4.getColumn()
                                block4=cell4.getBlock()

                                sharedcandidates=tempcandidates.intersection(candidates4)

                                if row4==row3 and cell4!=cell3 and len(sharedcandidates)>0:

                                    for cell5 in self.__puzzle.getKnowledge():

                                        candidates5=cell5.getCandidates()
                                        row5=cell5.getRow()
                                        column5=cell5.getColumn()
                                        block5=cell5.getBlock()

                                        sharedcandidates=tempcandidates.intersection(candidates5)

                                        if row5!=row3 and row5!=row and len(sharedcandidates)>0:

                                            tempcandidates=sharedcandidates

                                            for cell6 in self.__puzzle.getKnowledge():

                                                candidates6=cell6.getCandidates()
                                                row6=cell6.getRow()
                                                column6=cell6.getColumn()
                                                block6=cell6.getBlock()

                                                sharedcandidates=tempcandidates.intersection(candidates6) # most x wing conditions finally met (should take up three columns)
                                                rows=set((row,row2,row3,row4,row5,row6))
                                                columns=set((column,column2,column3,column4,column5,column6))

                                                if row6==row5 and cell6!=cell5 and len(sharedcandidates)==1 and len(columns)==3 and {(row,column),(row2,column2),(row3,column3),(row4,column4),(row5,column5),(row6,column6)} not in self.__resolved:

                                                    presentinrows=False
                                                    presentincolumns=False

                                                    for cell7 in self.__puzzle.getKnowledge(): # checking that the candidate only appears twice per row xor column (final condition)

                                                        candidates7=cell7.getCandidates()
                                                        row7=cell7.getRow()
                                                        column7=cell7.getColumn()

                                                        if len(sharedcandidates.intersection(candidates7))==1 and cell7!=cell6 and cell7!=cell5 and cell7!=cell4 and cell7!=cell3 and cell7!=cell2 and cell7!=cell:

                                                            if row7 in rows:

                                                               presentinrows=True

                                                            if column7 in columns:

                                                               presentincolumns=True

                                                    if presentinrows!=presentincolumns:

                                                        changemade=False

                                                        for cell7 in self.__puzzle.getKnowledge():

                                                            candidates7=cell7.getCandidates()
                                                            row7=cell7.getRow()
                                                            column7=cell7.getColumn()

                                                            if (row7 in rows or column7 in columns) and cell7!=cell6 and cell7!=cell5 and cell7!=cell4 and cell7!=cell3 and cell7!=cell2 and cell7!=cell:

                                                                oldcandidates=cell7.getCandidates()
                                                                self.__puzzle.updateKnowledge(sharedcandidates,row7,column7)
                                                                newcandidates=cell7.getCandidates()

                                                                if oldcandidates!=newcandidates:

                                                                    changemade=True

                                                        self.__resolved.append({(row,column),(row2,column2),(row3,column3),(row4,column4),(row5,column5),(row6,column6)})

                                                        if changemade==True:

                                                            return [{(row,column),(row2,column2),(row3,column3),(row4,column4),(row5,column5),(row6,column6)},sharedcandidates]

                                                    
                                            



            
    def makeMove(self,difficulty): # combine all the techniques to find a value that can be entered, then return partial solution

        move=[]
        solution=""
        maxdifficulty="easy"
        
        while move!=None:
            
            """try: # after each iteration update self.__resolved with the resolved pair/triple/quad
                self.__resolved.append(move[0])
            except IndexError:
                pass"""
            
            move=None
            
            move=self.nakedSingle()
            #print(move)
            if move!=None:
                solution+=f"Naked single: cell {move[0]} must be {move[1]}\n"
                return [solution,maxdifficulty]
            
            move=self.hiddenSingle()
            #print(move)
            if move!=None:
                solution+=f"Hidden single: cell {move[0]} must be {move[1]}\n"
                return [solution,maxdifficulty]
            
            move=self.nakedPair()
            #print(move)
            if move!=None:
                solution+=f"Naked pair at {move[0]}:\nremove {move[1]} from rest of intersection\n \n"
                continue
            
            move=self.hiddenPair()
            #print(move)
            if move!=None:
                solution+=f"Hidden pair at {move[0]}:\nset their candidates to only {move[1]}\n \n"
                continue

            if difficulty=="medium" or difficulty=="hard":

                maxdifficulty="medium"
            
                move=self.pointingPairOrTriple()
                #print(move)
                if move!=None:
                    solution+=f"Pointing pair/triple at {move[0]}:\nremove {move[1]} from the rest of the row/column\n \n"
                    continue
                
                move=self.nakedOrHiddenTriple()
                #print(move)
                if move!=None:
                    solution+=f"Naked/hidden triple at {move[0]}:\nremove {move[1]} from the rest of the row/column/block\n \n"
                    continue
                
                move=self.nakedOrHiddenQuad()
                #print(move)
                if move!=None:
                    solution+=f"Naked/hidden quad at {move[0]}:\nremove {move[1]} from the rest of the row/column/block\n \n"
                    continue

            if difficulty=="hard":

                maxdifficulty="hard"

                move=self.xWing()
                #print(move)
                if move!=None:
                    solution+=f"X-Wing at {move[0]}:\nremove {move[1]} from the rest of the rows/columns\n \n"
                    continue

                move=self.xyWing()
                #print(move)
                if move!=None:
                    solution+=f"XY-Wing or XYZ-Wing at {move[0]}:\nremove {move[1]} from cells intersecting both wings\n \n"
                    continue

                move=self.swordfish()
                #print(move)
                if move!=None:
                    solution+=f"Swordfish at {move[0]}:\nremove {move[1]} from any other cells in intersecting rows/columns\n \n"
                    continue
            
        return ["No value can be found in this arrangement\n",maxdifficulty]



    def solvePuzzle(self,difficulty): # repeat self.makeMove() until the puzzle is fully solved

        solved=False
        solution=""
        changemade=False
        meetsdifficulty=False
        
        while solved==False:
            
            self.__puzzle=Puzzle(self.__puzzle.getRows())
            self.__resolved=[]

            move=self.makeMove(difficulty)
            
            if move[0]=="No value can be found in this arrangement\n":
                    
                return "This puzzle cannot be solved"
            
            else:
                
                solution+=move[0]
                changemade=True
                
                if move[1]==difficulty:
                    meetsdifficulty=True
                
            board=self.__puzzle.getRows() # check for puzzle completion
            isComplete=True
            
            for row in board:
                for cell in row:
                    if cell=="_":
                        isComplete=False
                        
            if isComplete==True:
                solved=True
                
        return[board,solution,meetsdifficulty]
                    
            

        
