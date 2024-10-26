import pygame
import pyodbc
import time
import copy
from ai import *
from game import *
from knowledge import *



####################### """CLASSES FOR GUIS""" #########################


class Button: # for buttons

    def __init__(self,left,top,text="Dummy",width=200,height=80):

        self.text=font.render(text,True,(255,255,255))
        self.active=False
        self.clicked=False
        self.box=pygame.Surface((width,height))
        self.box.fill((100,100,100))
        self.rect=pygame.Rect(left,top,width,height)
        self.top=top
        self.left=left
        self.width=width
        self.height=height



    def draw(self,surface): # show button on screen and check if clicked

        self.active=False
        action=False
        screen.blit(self.box,(self.left,self.top))
        self.rect=pygame.Rect(self.left,self.top,self.width,self.height)
        mousepos=pygame.mouse.get_pos()

        if self.rect.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                action=True

        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        
        screen.blit(self.text,(self.left+5,self.top))

        return action






class TextInput: # for single char inputs in the puzzle

    def __init__(self,left,top,width,height,row,column,masked=False):

        self.text=""
        self.active=False
        self.width=width
        self.height=height
        self.textbox=pygame.Surface((width,height))
        self.textbox.fill((100,100,100))
        self.rect=pygame.Rect(left,top,width,height)
        self.top=top
        self.left=left
        self.row=row
        self.column=column
        self.candidates={"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,"9":False}
        self.maskedtext=""
        self.masked=masked



    def updateCandidates(self,puzzle,autocandidates): # calculate the candidates using the knowledge base when autocandidates is toggled on

        if self.text=="" and autocandidates==True:

            knowledge=Puzzle(puzzle)

            for cell in knowledge.getKnowledge():

                if self.row==cell.getRow() and self.column==cell.getColumn():

                    newcandidates=cell.getCandidates()
                    break

            self.candidates={"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,"9":False}
            
            for candidate in self.candidates:

                if candidate in newcandidates:

                    self.candidates[candidate]=True

        else:

            self.candidates={"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,"9":False}



    def reset(self): # resets all text in the text box to be empty

        self.text=""
        self.maskedtext=""
        self.candidates={"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,"9":False}



    def draw(self,surface): # show text box on screen and check if clicked

        if self.active==False:

            self.textbox.fill((100,100,100))

        else:

            self.textbox.fill((150,150,150))

        screen.blit(self.textbox,(self.left,self.top))
        self.rect=pygame.Rect(self.left,self.top,self.width,self.height)
        mousepos=pygame.mouse.get_pos()

        if self.rect.collidepoint(mousepos):
            
            if pygame.mouse.get_pressed()[0]==1 and self.active==False:
                
                self.active=True

        if self.text!="" and self.masked==False: # show normal text if not empty and not masked

            text=font.render(self.text,True,(255,255,255))
            screen.blit(text,(self.left,self.top))

        elif self.maskedtext!="" and self.masked==True: # show asterisks if not empty but masked

            text=font.render(self.maskedtext,True,(255,255,255))
            screen.blit(text,(self.left,self.top))

        else: # show candidates if empty (for LongTextInput no candidates will ever be displayed since they are always False)

            candidatepos={"1":(self.left+5,self.top+3),"2":(self.left+29,self.top+3),"3":(self.left+51,self.top+3),
                          "4":(self.left+5,self.top+26),"5":(self.left+29,self.top+26),"6":(self.left+51,self.top+26),
                          "7":(self.left+5,self.top+48),"8":(self.left+29,self.top+48),"9":(self.left+51,self.top+48)}

            for candidate in self.candidates:

                if self.candidates[candidate]==True:

                    text=smallfont.render(candidate,True,(255,255,255))
                    screen.blit(text,candidatepos[candidate])

        return self.active



    def write(self): # let user enter character if clicked

        global userpuzzle

        if self.active==True:
            
            for event in pygame.event.get():
                
                if event.type==pygame.KEYDOWN:
                    
                    try:
                        
                        if ord(event.unicode) in range(49,58):
                            
                            self.text=event.unicode
                            userpuzzle[self.row][self.column]=self.text
                            text=font.render(self.text,True,(255,255,255))
                            screen.blit(text,(self.left+5,self.top+5))
                            self.rect=pygame.Rect(self.left,self.top,70,70)
                            global solution
                            return isComplete(userpuzzle,solution) # if puzzle now complete after entering value, return True

                        if event.key==pygame.K_BACKSPACE:

                            self.text=""
                            userpuzzle[self.row][self.column]="_"
                        
                    except TypeError: # handle error from user pressing special keys
                        
                        return False

        elif self.text!="": # to check for completion when value entered by AI rather than user

            userpuzzle[self.row][self.column]=self.text
            return isComplete(userpuzzle,solution)




                            

class LongTextInput(TextInput): # for inputs of variable size

    def __init__(self,left,top,width,height,row=0,column=0,masked=False):
        
        super().__init__(left,top,width,height,row,column,masked)



    def write(self,screen): # let user enter any length string

        super().draw(screen)
        
        if self.active==True:
            
            for event in pygame.event.get():
                
                if event.type==pygame.KEYDOWN:
                    
                    try:
                        
                        if ord(event.unicode) in range(33,126):
                            
                            self.text+=event.unicode
                            self.maskedtext+="*"
                            
                        if event.key==pygame.K_BACKSPACE:
                            
                            self.text=self.text[:-1]
                            self.maskedtext=self.maskedtext[:-1]
                            
                    except: # error handling for when special key pressed
                        
                        pass




######################### """SUBROUTINES""" #########################


def newPuzzle(difficulty): # create a new puzzle from the templates and update variables accordingly

    puzzle=generatePuzzle(difficulty)
    
    while puzzle==None:
        puzzle=generatePuzzle(difficulty)
        
    global initialpuzzle
    global userpuzzle
    global solution
    initialpuzzle=copy.deepcopy(puzzle[0])
    userpuzzle=copy.deepcopy(puzzle[0])
    solution=puzzle[1]
    displayPuzzle(initialpuzzle)


        
def displayPuzzle(puzzle): # create the list of numbers and TextInput objects to be displayed for the puzzle

    global squares
    for row in range(len(puzzle)):
        for column in range(len(puzzle[row])):
            if puzzle[row][column]=="_":
                squares.append(TextInput(50+column*73,30+row*73, 70,70,row,column))
            else:
                squares.append((font.render(puzzle[row][column],True,(255,255,255)),50+column*73,30+row*73))



def isComplete(puzzle,solution): # check for puzzle completion

    if puzzle==solution:
        return True
    return False



def calculateScore(timetaken,aimoves,difficulty,autocandidatesused): # calculate score from 0-100 based on given parameters

    minutes=timetaken//60
    timepoints=(-1/1500)*(minutes**3)+50
    
    if timepoints<0:
        timepoints=0

    aipoints=(-5)*(aimoves**(3/2))+50

    if aipoints<-50:
        aipoints=-50

    score=timepoints+aipoints
    if difficulty=="easy":
        score*=0.5
    elif difficulty=="medium":
        score*=0.75

    if autocandidatesused==True:

        score*=0.5

    return int(score)



def puzzleToString(puzzle): # format 2d list into string so that puzzle can be stored in database

    string=""

    for row in puzzle:

        for cell in row:

            string+=cell

    return string



def downloadPuzzle(puzzleid,username,initialstate,finalstate,score): # format puzzle (81 char string) from database into text file

    date=time.localtime(puzzleid)
    filename=time.strftime("%Y-%m-%d %H.%M.%S",date)

    file=open(f"{filename}.txt","w")

    text=f"Puzzle completed by {username} on {filename}\nScore: {score}\n\n"

    for char in range(len(initialstate)):

        text+=f"{initialstate[char]} "

        if (char+1)%27==0 and char!=80:

            text+="\n---------------------\n"

        elif (char+1)%9==0:

            text+="\n"

        elif (char+1)%3==0 and char!=80:

            text+="| "

    text+="\n"

    for char in range(len(finalstate)):

        text+=f"{finalstate[char]} "

        if (char+1)%27==0 and char!=80:

            text+="\n---------------------\n"

        elif (char+1)%9==0:

            text+="\n"

        elif (char+1)%3==0 and char!=80:

            text+="| "

    file.write(text)

    file.close()



######################## """MAIN PROGRAM""" ###################



if __name__=="__main__":

    """Try to connect to SQL Server"""

    online=True
    print("Trying to connect to server...")

    try:

        #raise Exception # <-- uncomment one of these to skip connection process for test purposes
        #pass
        connection=pyodbc.connect("DRIVER={SQL Server};SERVER=*****;PORT=*****;Database=SudokuTrainer;UID=*****;PWD=*****;",autocommit=False) # censored ip etc because this was hosted on my home pc
        cursor=connection.cursor() # create pyodbc connection and cursor
        print("Successfully connected to server")

    except:

        online=False
        print("Failed to connect to server, proceeding offline")

    time.sleep(1)




        


    """Initialise variables"""

    pygame.init()

    screenwidth=1280 # create game window
    screenheight=720
    screen=pygame.display.set_mode((screenwidth,screenheight))
    pygame.display.set_caption("Sudoku Trainer - Menu")

    font=pygame.font.SysFont("verdana",60) #define fonts
    smallfont=pygame.font.SysFont("verdana",15)

    textcolour=(255,255,255) # define colours

    playbutton=Button(572,400,"Play",135,80) # initialise buttons
    aimovebutton=Button(710,120,"AI Move",255,80)
    autocandidatesbutton=Button(710,30,"Toggle Candidates",555,80)
    accountbutton=Button(515,580,"Account",250,80)
    menubutton=Button(1095,10,"Menu",175,80)
    instructionsbutton=Button(455,490,"Instructions",370,80)
    signinbutton=Button(17,540,"Sign In",230,80)
    signupbutton=Button(10,450,"Sign Up",245,80)
    signoutbutton=Button(10,630,"Sign Out",275,80)
    easybutton=Button(270,400,"Easy",155,80)
    mediumbutton=Button(490,400,"Medium",245,80)
    hardbutton=Button(810,400,"Hard",155,80)
    puzzlebuttons=[Button(900,250,"Puzzle 1",270,80),Button(900,340,"Puzzle 2",270,80),Button(900,430,"Puzzle 3",270,80)]

    usernameinput=LongTextInput(10,100,800,80) # initialise text boxes
    passwordinput=LongTextInput(10,300,800,80,0,0,True)

    ingame=False # game variables
    inaccount=False
    indifficulty=False
    inscore=False
    ininstructions=False
    gametime=time.time()
    gameaimoves=0
    initialpuzzle=[]
    userpuzzle=[]
    solution=[]
    squares=[]
    difficulty="easy"
    username=""
    password=""
    puzzlescompleted=0
    bestscore=-999
    averagescore=-999
    averageaimoves=-999
    loggedin=False
    messages=[]
    autocandidates=False
    autocandidatesused=False
    solutiontext=[]
    onlinemessage=False
    downloadmessage=""












    """Main game loop"""

    game=True

    while game==True:


        """In-game screen where puzzle is displayed"""

        if ingame==True:

            pygame.display.set_caption("Sudoku Trainer - In Game")
            timetaken=int(time.time()-gametime)
            
            screen.fill((0,0,0))

            
            
            if aimovebutton.draw(screen)==True: # when AI Move button clicked, update variables, update text box for cell, check for puzzle completion

                gameaimoves+=1
                ai=SudokuAI(userpuzzle)
                aipuzzle=ai.getPuzzle().getRows()
                solutiontext=ai.makeMove(difficulty)[0].split("\n")
                del solutiontext[-1]             
                
                for row in range(len(aipuzzle)):
                    
                    for column in range(len(aipuzzle[row])):
                        
                        if aipuzzle[row][column]!="_":
                            
                            for square in squares:
                                
                                if isinstance(square,TextInput):
                                    
                                    if square.row==row and square.column==column:
                                        
                                        square.text=aipuzzle[row][column]
                                        
                                        if square.write()==True:

                                            ingame=False
                                            break
                userpuzzle=aipuzzle
                

                
            if autocandidatesbutton.draw(screen)==True: # toggle automatic candidates on/off when Toggle Candidates button clicked

                autocandidates=(not autocandidates)
                autocandidatesused=True

                
            
            if timetaken%60<10: # display timer and ai move counter
                
                counters=smallfont.render(f"Time elapsed: {timetaken//60}:0{timetaken%60}   AI Moves: {gameaimoves}",True,(255,255,255))
                
            else:

                counters=smallfont.render(f"Time elapsed: {timetaken//60}:{timetaken%60}   AI Moves: {gameaimoves}",True,(255,255,255))
                
            screen.blit(counters,(710,650))
            


            temptexty=250 # display steps of AI Move

            for text in solutiontext:

                temptext=smallfont.render(text,True,(255,255,255))
                screen.blit(temptext,(710,temptexty))
                temptexty+=20


            
            for square in squares: # display puzzle to screen, let user write to text boxes, check for puzzle completion
                
                if isinstance(square,TextInput):

                    square.updateCandidates(userpuzzle,autocandidates)
                    
                    if square.draw(screen)==True:
                        
                        if square.write()==True:
                            
                            ingame=False
                            break
                else:
                    
                    screen.blit(square[0],(square[1],square[2]))



            horizontalline=pygame.Surface((654,3)) # add lines to divide puzzle into 3x3 blocks
            horizontalline.fill((255,255,255))
            verticalline=pygame.Surface((3,654))
            verticalline.fill((255,255,255))
            screen.blit(horizontalline,(50,246))
            screen.blit(horizontalline,(50,465))
            screen.blit(verticalline,(266,30))
            screen.blit(verticalline,(485,30))
            


            if pygame.mouse.get_pressed()[0]==1: # check if active cell clicked out of, set active attribute to False if so

                for square in squares:

                    if isinstance(square,TextInput):

                        mousepos=pygame.mouse.get_pos()

                        if square.rect.collidepoint(mousepos)==False:

                            square.active=False
                        

                    
            if ingame==False: # when the puzzle is finished or exited, reset variables, calculate score, update database
                
                squares=[]
                solutiontext=[]
                
                puzzlescompleted+=1
                timetaken=int(time.time()-gametime)
                gamescore=calculateScore(timetaken,gameaimoves,difficulty,autocandidatesused)
                if gamescore>bestscore:
                    bestscore=gamescore
                averagescore=(averagescore*(puzzlescompleted-1)+gamescore)/puzzlescompleted
                averageaimoves=(averageaimoves*(puzzlescompleted-1)+gameaimoves)/puzzlescompleted

                autocandidates=False
                autocandidatesused=False


                if online==True: # update account statistics
                
                    cursor.execute(f"UPDATE Accounts SET PuzzlesCompleted={puzzlescompleted}, BestScore={bestscore}, AverageScore={averagescore}, AverageAIMoves={averageaimoves} WHERE Username='{username}'")
                    connection.commit()

                    if loggedin==True: # add new puzzle to database

                        cursor.execute(f"INSERT INTO Puzzles (PuzzleID, Username, InitialState, FinalState, Score) VALUES ({time.time()},'{username}','{puzzleToString(initialpuzzle)}','{puzzleToString(userpuzzle)}',{gamescore})")
                        #connection.commit()

                        puzzles=cursor.execute(f"SELECT * FROM Puzzles WHERE Username='{username}' ORDER BY PuzzleID DESC")
                        
                        puzzlecount=0

                        for row in puzzles: # delete old puzzles from database

                            puzzlecount+=1

                            if puzzlecount>3:
                                
                                puzzleid=row.PuzzleID
                                cursor.execute(f"DELETE FROM Puzzles WHERE PuzzleID='{puzzleid}'")
                                connection.commit()
                            

                inscore=True # head to score screen









        elif inaccount==True and online==True: # account screens






            """Sign in/ up screen"""

                
            if loggedin==False:
                
                screen.fill((0,0,0))
                pygame.display.set_caption("Sudoku Trainer - Account")

                
                
                if menubutton.draw(screen)==True: # return to menu and reset variables if Menu button clicked
                    
                    time.sleep(0.1)
                    inaccount=False
                    usernameinput.reset()
                    passwordinput.reset()
                    messages=[]


                    
                text=font.render("Username",True,(255,255,255)) # display Username and Password headings, let the user write to text boxes
                screen.blit(text,(10,10))
                text=font.render("Password",True,(255,255,255))
                screen.blit(text,(10,220))
                usernameinput.write(screen)
                passwordinput.write(screen)


                
                if signinbutton.draw(screen)==True: # if sign in button clicked, check database for account details entered

                    messages=["No account with these credentials exists."]
                    
                    credentials=cursor.execute(f"SELECT * FROM Accounts WHERE Username='{usernameinput.text}' AND Password='{passwordinput.text}'")
                    
                    for row in credentials: # update variables and log in if account found, do nothing (will display message) if account not found
                        
                        username=row.Username
                        password=row.Password
                        puzzlescompleted=row.PuzzlesCompleted
                        bestscore=row.BestScore
                        averagescore=row.AverageScore
                        averageaimoves=row.AverageAIMoves
                        loggedin=True
                        messages=[]
                        usernameinput.reset()
                        passwordinput.reset()



                if pygame.mouse.get_pressed()[0]==1: # check if active text box clicked out of and set active attribute to False if so

                        mousepos=pygame.mouse.get_pos()

                        if usernameinput.rect.collidepoint(mousepos)==False:

                            usernameinput.active=False

                        if passwordinput.rect.collidepoint(mousepos)==False:

                            passwordinput.active=False



                if signupbutton.draw(screen)==True: # if sign up button clicked, check if details match constraints, read strings to see each constraint

                    messages=[]

                    validcredentials=True

                    usernamecheck=cursor.execute(f"SELECT Username FROM Accounts WHERE Username='{usernameinput.text}'")

                    for row in usernamecheck:

                        if row.Username==usernameinput.text:

                            messages.append("Username is already taken.")
                            validcredentials=False

                    if len(usernameinput.text) not in range(3,20):

                        messages.append("Username needs to be between 3 and 20 characters.")
                        validcredentials=False

                    for char in usernameinput.text:

                        if ord(char) not in range(65,90) and ord(char) not in range(97,122) and ord(char) not in range(48,57) and char!="_":

                            messages.append("Username can only contain numbers, English letters or underscores.")
                            validcredentials=False
                            break

                    if len(passwordinput.text)<8:

                        messages.append("Password needs to be at least 8 characters.")
                        validcredentials=False

                    if validcredentials==True: # if all constraints satisfied, add account to database, update variables, sign in

                        cursor.execute(f"INSERT INTO Accounts (Username,Password,PuzzlesCompleted,BestScore,AverageScore,AverageAIMoves) VALUES ('{usernameinput.text}','{passwordinput.text}',0,0,0,0)")
                        connection.commit()
                        username=copy.deepcopy(usernameinput.text)
                        password=copy.deepcopy(passwordinput.text)
                        usernameinput.reset()
                        passwordinput.reset()
                        puzzlescompleted=0
                        bestscore=0
                        averagescore=0
                        averageaimoves=0
                        loggedin=True
                        messages=[]

                        

                if len(messages)>0: # display any messages regarding failed sign in / sign up

                    tempycoord=400
                    
                    for i in messages:

                        tempycoord+=50
                        message=smallfont.render(i,True,(255,255,255))
                        screen.blit(message,(350,tempycoord))

                        

                blackbox=pygame.Surface((500,300)) # black surface to cover text that goes out of text boxes
                blackbox.fill((0,0,0))
                screen.blit(blackbox,(810,100))

                    






            """Sign out screen including account statistics and puzzle download"""

                
            if loggedin==True:
                
                screen.fill((0,0,0))
                pygame.display.set_caption("Sudoku Trainer - Account")

                
                
                if menubutton.draw(screen)==True: # return to menu if Menu button clicked
                    
                    time.sleep(0.1)
                    inaccount=False
                    downloadmessage=""


                    
                text=font.render(f"Welcome, {username}",True,(255,255,255)) # display account statistics
                screen.blit(text,(10,10))
                
                text=font.render(f"Puzzles completed: {puzzlescompleted}",True,(255,255,255))
                screen.blit(text,(10,100))
                
                text=font.render(f"Best score: {bestscore}",True,(255,255,255))
                screen.blit(text,(10,190))

                text=font.render(f"Average score: {round(averagescore,2)}",True,(255,255,255))
                screen.blit(text,(10,280))

                text=font.render(f"Average AI Moves: {round(averageaimoves,2)}",True,(255,255,255))
                screen.blit(text,(10,370))

                text=smallfont.render(f"Download your latest puzzles: ",True,(255,255,255))
                screen.blit(text,(900,200))

                text=smallfont.render(downloadmessage,True,(255,255,255)) # if puzzle was downloaded then display success message
                screen.blit(text,(900,225))

                

                puzzles=cursor.execute(f"SELECT * FROM Puzzles WHERE Username='{username}' ORDER BY PuzzleID DESC")

                puzzlebuttoncount=-1 # show buttons to download last 3 puzzles

                for row in puzzles:

                    puzzlebuttoncount+=1

                    if puzzlebuttons[puzzlebuttoncount].draw(screen)==True:

                        downloadPuzzle(row.PuzzleID,row.Username,row.InitialState,row.FinalState,row.Score)
                        downloadmessage=f"Downloaded puzzle {puzzlebuttoncount+1} successfully."

                        
                
                if signoutbutton.draw(screen)==True: # if Sign Out button clicked, reset variables and sign out
                    
                    loggedin=False
                    username=""
                    password=""
                    puzzlescompleted=0
                    bestscore=0
                    averagescore=0
                    averageaimoves=0
                    time.sleep(0.1)
                    downloadmessage=""
            





            """Difficulty selection screen"""


        elif indifficulty==True:
            
            screen.fill((0,0,0))
            pygame.display.set_caption("Sudoku Trainer - Selecting Difficulty")
            text=font.render("Select difficulty...",True,(255,255,255))
            screen.blit(text,(360,100))

            

            if easybutton.draw(screen)==True: # generate puzzle of corresponding difficulty, reset some variables, go to game/puzzle screen

                difficulty="easy"
                newPuzzle(difficulty)
                ingame=True
                indifficulty=False
                gametime=time.time()
                gameaimoves=0

                

            elif mediumbutton.draw(screen)==True:

                difficulty="medium"
                newPuzzle(difficulty)
                ingame=True
                indifficulty=False
                gametime=time.time()
                gameaimoves=0

                

            elif hardbutton.draw(screen)==True:

                difficulty="hard"
                newPuzzle(difficulty)
                ingame=True
                indifficulty=False
                gametime=time.time()
                gameaimoves=0




            """Post-game score screen"""

        elif inscore==True: # display score to user after completing puzzle

            screen.fill((0,0,0))
            pygame.display.set_caption("Sudoku Trainer - Puzzle Completed")
            message=font.render(f"Puzzle Completed! Score: {gamescore}",True,(255,255,255))
            screen.blit(message,(200,330))

            
            
            if menubutton.draw(screen)==True: # return to menu if Menu button clicked

                inscore=False





            """Instructions screen"""

        elif ininstructions==True:

            screen.fill((0,0,0))
            pygame.display.set_caption("Sudoku Trainer - Reading Instructions") # display set of text instructions

            
            
            text=smallfont.render("In Sudoku, there is a 9x9 grid subdivided into rows, columns, and 3x3 blocks.",True,(255,255,255))
            screen.blit(text,(100,100))

            text=smallfont.render("Your goal is to fill this grid so that each digit from 1 to 9 appears exactly once in every row, column, and block.",True,(255,255,255))
            screen.blit(text,(100,150))

            text=smallfont.render("Try to complete the puzzle quickly to get more points!",True,(255,255,255))
            screen.blit(text,(100,200))

            text=smallfont.render("You can select different difficulties. Harder puzzles let you achieve more points.",True,(255,255,255))
            screen.blit(text,(100,250))

            text=smallfont.render("If you are stuck, you can press the Toggle Candidates button to see the possible values for every cell.",True,(255,255,255))
            screen.blit(text,(100,300))

            text=smallfont.render("If you are still stuck, you can press the AI Move button to let the AI fill in a cell and help you.",True,(255,255,255))
            screen.blit(text,(100,350))

            text=smallfont.render("The AI will explain the move it made to help you get better. Why not research the techniques on the internet?",True,(255,255,255))
            screen.blit(text,(100,400))

            text=smallfont.render("However, using these tools will reduce your score.",True,(255,255,255))
            screen.blit(text,(100,450))

            text=smallfont.render("Cells are given coordinates based on their horizontal then vertical position from 0 to 8.",True,(255,255,255))
            screen.blit(text,(100,500))

            text=smallfont.render("Create an account to keep track of your scores and download older puzzles!",True,(255,255,255))
            screen.blit(text,(100,550))

            

            if menubutton.draw(screen)==True: # return to menu if Menu button clicked

                ininstructions=False

            

        
        

            """Main menu screen"""


        else:
            
            screen.fill((0,0,0))



            if playbutton.draw(screen)==True: # head to difficulty screen if Play button clicked, reset online message
                
                time.sleep(0.2)
                indifficulty=True
                onlinemessage=False

                

            if accountbutton.draw(screen)==True: # if Account button clicked, head to account screen if online, display failure message if offline
                
                if online==True:
                
                    time.sleep(0.1)
                    inaccount=True

                else:

                    onlinemessage=True

                    

            if instructionsbutton.draw(screen)==True: # head to instructions screen if Instruction button clicked, reset online message

                ininstructions=True
                onlinemessage=False

                

            if onlinemessage==True: # display failure message if offline and Account button was clicked
                    
                text=smallfont.render("Cannot access account in offline mode.",True,(255,255,255))
                screen.blit(text,(490,250))

                
            
            pygame.display.set_caption("Sudoku Trainer - Menu")    
            text=font.render("Sudoku Trainer",True,(255,255,255))
            screen.blit(text,(410,100))



        



        for event in pygame.event.get(): # end loop if user quits
            
            if event.type==pygame.QUIT:
                
                game=False



        pygame.display.update() # refresh display



