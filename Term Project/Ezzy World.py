#Ezzy World
#Term Project
#Danielle Hu + Section O

from eventBasedAnimationClass import EventBasedAnimationClass
from Tkinter import *
import random
import time
import string
import os


class runGame(EventBasedAnimationClass):
    def __init__(self):
        self.width, self.height = 1000, 650
        super(runGame, self).__init__(self.width, self.height)

    def initAnimation(self):
        #Called at beginning of the game to initialize everything
        self.Ezzies = []
        self.furnitureList = []
        self.space = []
        #self.space in form (x, y, xr, yr, index in FurnitureList)
        #keeps track of where furniture is in the room
        self.helperInit()
        self.personalityList = ["ezzy.rebel.gif", "ezzy.normal.gif",
                                "ezzy.nerd.gif"]
        self.initiateMenus()
        self.drawCreateEzzy()
        self.initiateEventBinds()

    def helperInit(self):
        #Initialize variables
        self.needtimeMax, self.middleY, self.middleX = 25, 260, 500
        self.gameHeight, self.barX, self.ezzyH= 525, 125, 490
        self.create, self.help, self.Action = False, False, False
        self.selectorIndex, self.selectedMove = None, None
        self.selector, self.selectorCount, self.count = False, 0, 0
        self.selectedFurniture, self.doAnimation = None, False
        self.selectText, self.menuCount, self.randomTextIndex = None, 0, 0
        self.timerDelay, self.xradius, self.yradius = 1000, 0, 0
        self.menuStatus, self.moodText, self.automaticEzzy = True, 1, None
        self.editMode, self.createStatus, self.isLegal = False, False, True
        self.currentEzzy, self.selectAge, self.selectedAge = True, False, None
        self.selectedEzzy,self.ezzyIndex,self.createComplete = None, None, None
        self.displayCreateBG, self.displayCreateName = False, False
        self.pickPersonality, self.selectedPersonality = False, None
        self.personalityAction, self.moodCount, self.moodyEzzy = None, 0, None
        self.money, self.cost, self.deltaX, self.deltaY = 100, 10, 50, 50
        self.twerkPlay, self.parkPlay, self.createComple = False, False, None
        self.town, self.twerk, self.park, self.counter = False, False, False, 0
        self.saveload, self.loaded = False, False

    def initiateEventBinds(self):
        #Binds extra events to functions
        self.root.bind("<Motion>", lambda event: self.onMouseMotion(event))
        self.root.bind("<B1-Motion>", lambda event: self.onPressedMotion(event))
        self.root.bind("<ButtonRelease-1>", lambda event: self.releasePM())
        self.root.bind("<Button-3>", lambda event: self.onRMousePressed(event))


    #readFile and writeFile were both taken from 15-112 Course Notes
    def readFile(self, filename, mode="rt"):
    # Reads a text file and returns the contents
    # rt = "read text"
        with open(filename, mode) as fin:
            return fin.read()

    def writeFile(self, filename, contents, mode="wt"):
    # Creates and writes a text file if there isn't one already
    # Writes and replaces text file if there's already one
    # wt = "write text"
        with open(filename, mode) as fout:
            fout.write(contents)

    def loadFile(self):
        # Loads features of a saved game based on file I/O
        if os.path.exists("savedEzzy.txt"):
        #if there is a saved file:
            loadFile = self.readFile("savedEzzy.txt")
        
            #Line 1: Generate Ezzies
            endLine = loadFile.index("\n")
            loadTemp = loadFile[:endLine]
            loadEzzies = eval(loadTemp)
            for i in xrange(len(loadEzzies)):
                x, y, name, personality, age = loadEzzies[i]
                newEzzy = Ezzy(x, y, name, personality, age)
                self.Ezzies.append(newEzzy)

            #Line 2: Generate Furniture
            loadFile = loadFile[endLine+1:]
            endLine = loadFile.index("\n")
            loadFurniture = eval(loadFile[:endLine])
            for i in xrange(len(loadFurniture)):
                furnIndex, x, y = loadFurniture[i]
                newFurniture = Furniture(furnIndex, x, y)
                self.furnitureList.append(newFurniture)
            
            #Line 3: Load Money
            loadFile = loadFile[endLine+1:]
            endLine = loadFile.index("\n")
            self.money = int(eval(loadFile[:endLine]))

            #Line 4: Load Space
            loadFile = loadFile[endLine+1:]
            endLine = loadFile.index(".")
            self.space = eval(loadFile[:endLine])

            #Select first Ezzy in list
            self.selectedEzzy = self.Ezzies[0]

    def saveFile(self):
        #Save contents into a text file that will be used to load a game
        contents = ""
        index = 0
        saveEzzies = [] #["x", "y", "name", "personality", "age"]
        saveFurniture = [] #["furniture index", "x", "y"]

        for ezzyIndex in xrange(len(self.Ezzies)):
            ezzy = self.Ezzies[ezzyIndex]
            saveEzzies.append([ezzy.x, ezzy.y, ezzy.name[:-1],
                               ezzy.personality, ezzy.age])
        for fIndex in xrange(len(self.furnitureList)):
            furn = self.furnitureList[fIndex]
            saveFurniture.append([furn.furnIndex, furn.x, furn.y])
            
        contents += (str(saveEzzies) + "\n" + str(saveFurniture) +
                     "\n" + str(self.money) + "\n" + str(self.space) + ".")
        #Contents (in order): Ezzies, Furniture, Money, Space
        for i in contents:
            #replaces " with ' to be able to evaluate lists and strings
            if i == '"': contents = contents[:index] + "'" + contents[index+1:]
            index += 1
        self.writeFile("savedEzzy.txt", contents)
    
    def createObj(self):
        #Creates Ezzies at the center of the board with the customized traits
        #Appends it to a list of Ezzies to be accessed later
        newEzzy = Ezzy(self.width, self.height, self.entryName,
                       self.selectedPersonality, self.selectedAge)
        self.Ezzies.append(newEzzy)
        self.selectedPersonality = None
        self.selectAge, self.displayCreateBG = False, False

    def helpScreen(self): #Displays help screen
        if self.help == True:
            self.drawHelp()

    def releasePM(self):
        #In regards to moving furniture: Once mouse is released, deselect furn.
        self.selectedMove = None
        
    def onPressedMotion(self, event): ########### PRESSED MOTION ###########
        #Event: When mouse is both pressed and moving: move furniture
        xInd, yInd, xrInd, yrInd = 0, 1, 2, 3
        if self.editMode == True and self.selectedMove == None:
            #select furniture to edit
            for i in xrange(len(self.furnitureList)):
                #for each furniture in space, find
                #whether a click was on a piece of furniture
                x, y = self.space[i][xInd],self.space[i][yInd]
                x_r, y_r = self.space[i][xrInd],self.space[i][yrInd]
                if (event.x > x-x_r and event.x < x+x_r and
                    event.y > y-y_r and event.y < y+y_r):
                    self.selectedMove = self.furnitureList[self.space[i][4]]
                    break
        if self.selectedMove != None:
            #Once a piece of furniture is found, set the selected
            #furniture's coordinates to the motioned mouse
            self.selectedMove.x = event.x
            self.selectedMove.y = event.y
                    
    def onKeyPressed(self, event): ########### KEY PRESSED ###########
        #Set variables based on key press
        if self.twerk or self.park: self.keyPressedTown(event)
        else:
            #Edit Mode
            if len(self.furnitureList) >= 1 and self.createStatus == False:
                if event.char == "e":
                    self.editMode = True if self.editMode == False else False

            #Create Mode
            if self.createStatus == True and self.displayCreateName == True:
                if event.keysym == "Return":
                    self.createComplete, self.displayCreateName = True, False
                    self.pickPersonality = True
                if event.keysym == "BackSpace":
                    self.entryName = self.entryName[0:len(self.entryName)-1]
                else: self.entryName += event.char

            #Game Mode to access town or menu screens
            if self.createStatus == False:
                if event.char == "t":
                    self.town = True if self.town == False else False
            if event.keysym == "Escape":
                self.menuStatus = True if self.menuStatus == False else False

    def keyPressedTown(self, event):
        if (self.town == False and (self.twerk == True or self.park == True)):
            if event.keysym=="Escape":
                self.twerk = self.park = False
                self.money = int(self.money)
                self.gameFired, self.timerFired = False, True
            elif self.twerk:
                if self.twerkInstructions == True:
                    if event.char != None or event.keysym != None:
                        self.twerkStart = True
                        self.twerkInstructions = False
                elif self.twerkStart == True:
                    if event.keysym == "space":
                        self.twerkStart = False
                        self.twerkPlay = True
                elif event.keysym == "BackSpace" and len(self.userInput) > 0:
                    self.userInput = self.userInput[0:len(self.userInput)-1]
                else: self.userInput += event.char
            elif self.park:
                if self.parkInstructions == True:
                    if event.char != None or event.keysym != None:
                        self.parkStart, self.parkInstructions = True, False
                elif self.parkStart:
                    if event.keysym == "space":
                        self.parkStart, self.parkPlay = False, True
            
    def onMousePressed(self, event):  ########### LMOUSE PRESSED ###########
        #Carry out actions based on left click of mouse
        if self.menuCount == 1: self.menuCount, self.saveload = 0, False
        if self.menuStatus == True: self.displayMenus(event)
        if (event.x > 0 and event.x < self.barX and event.y > self.gameHeight):
            #Menu button
            if self.menuStatus == False: self.menuStatus = True
            else: self.menuStatus, self.menuCount = False, 0
        elif (event.x > self.barX and event.x < self.barX*2 and
            event.y > self.gameHeight and event.y < self.height and
            self.editMode == False and self.createStatus ==
            False and (self.money-self.cost*2 >= 0)):
            #Create button
            self.createStatus = True
            self.money -= self.cost*2
            self.displayCreate()
        elif (event.x > 0 and event.y > 0 and event.x < self.width and event.y <
            self.gameHeight and self.selectorCount==0 and self.editMode ==
            False and self.createStatus == False and len(self.Ezzies) >
            0 and self.town == False and self.menuStatus == False):
            #Move selected Ezzy if somewhere in the room was clicked
            self.drawMotion(event.x, event.y, self.selectedEzzy)
        elif (event.x > self.barX*2 and event.x < self.barX*3 and
            self.createStatus == False and event.y >
            self.gameHeight and event.y < self.height):
            #Shop button
            self.selector, self.selectorCount = True, 1
        self.onMousePressedHelper(event)

    def onMousePressedHelper(self, event):
        #Helper of Mouse Pressed:
        #Handles extra features (create & town screens)
        self.mouseFurniture(event)
        if self.pickPersonality == True: self.pickPersonalityMouse(event)
        if self.selectAge == True: self.pickAgeMouse(event)
        if self.town == True: self.selectGame(event)

    def displayMenus(self, event):
        x1, x2 = 440, 560
        about_y1, about_y2 = 160, 200
        ezzy_y1, ezzy_y2 = 230, 280
        help_y1, help_y2, = 300, 345
        save_y1, save_y2, load_y1, load_y2 = 370, 410, 440, 475
        #display screens from the menu or carry out load/save
        if event.x > x1 and event.x < x2 and self.menuCount != 1:
            if event.y > about_y1 and event.y < about_y2:
                self.menuScreen = PhotoImage(file="menu.about.gif")
                self.menuCount = 1
            if event.y > ezzy_y1 and event.y < ezzy_y2:
                self.menuScreen = PhotoImage(file="menu.ezzy.gif")
                self.menuCount = 1
            elif event.y > help_y1 and event.y < help_y2:
                self.menuScreen = PhotoImage(file="menu.help.gif")
                self.menuCount = 1
            elif event.y > save_y1 and event.y < save_y2:
                self.saveFile()
                self.saveload = True
            elif (event.y > load_y1 and event.y < load_y2 and
                  self.loaded != True):
                self.loadFile()
                self.saveload = True
                self.loaded = True
        
    def selectGame(self, event):
        #Selects mini-game and initializes conditions
        t_x1, t_x2, y1, y2 = 45, self.middleY, 80, self.middleX
        p_x1, p_x2 = 750, 950
        if event.x > t_x1 and event.x < t_x2 and event.y > y1 and event.y < y2:
            #Initialize mini-game "Get Twerk"
            self.twerk, self.twerkInstructions = True, True
            self.advance = True
            self.currentLevel = 1
            self.maxLevel = 10
            self.twerkStart, self.twerkPlay = False, False
            self.twerkLose, self.twerkWin = False, False
            self.town = False
        elif event.x>p_x1 and event.x<p_x2 and event.y > y1 and event.y < y2:
            #Initialize mini-game "Pedestal Park"
            self.park, self.parkInstructions = True, True
            self.parkStart, self.parkPlay, self.parkOver = False, False, False
            self.humanX, self.humanY, self.humanR = 500, 260, 25
            self.parkTimer = 10
            self.previousMoney = self.money
            self.town = False
            self.timerFired = False
            
    def pickAgeMouse(self, event):
        #Select a young personality Ezzy or an old personality Ezzy
        x_r, y_r = 50, 60
        y, youngX, oldX = 360, 170, 830
        if event.y > y-y_r and event.y < y+y_r:
            if event.x > youngX - x_r and event.x < youngX + x_r: #young
                self.selectedAge = 0
                self.createObj()
                self.selectedEzzy = self.Ezzies[-1]
                self.selectAge, self.createStatus = False, False
            elif event.x > oldX - x_r and event.x < oldX + x_r: #old
                self.selectedAge = 1
                self.createObj()
                self.selectedEzzy = self.Ezzies[-1]
                self.selectAge, self.createStatus = False, False
                
    def pickPersonalityMouse(self, event):
        #Select a personality Ezzy: Rebel of Nerd
        x_r, y_r = 50, 60
        y, x = 390, 250
        if event.y > y-y_r and event.y < y+y_r:
            for i in xrange(3):
                if (event.x > x+(x*i)-x_r and event.x < x+(x*i)+x_r):
                    self.selectedPersonality = i
                    self.selectAge = True
                    self.pickPersonality = False
                    break
        
    def mouseFurniture(self, event):
        #Choose and place furniture in the room
        self.placeFurniture(event)
        self.chooseFurniture(event)
        if self.selectedFurniture != None and self.count == 1:
            self.checkSelection(event)

    def onRMousePressed(self, event): ########### RMouse PRESSED ###########
        #select and carry actions for furniture
        for i in xrange(len(self.furnitureList)):
            #if nothing has been selected yet, check if the click selects
            x, y = self.space[i][0],self.space[i][1]
            x_r, y_r = self.space[i][2],self.space[i][3]
            if (event.x > x-x_r and event.x < x+x_r and
                event.y > y-y_r and event.y < y+y_r): #select
                index = self.space[i][4]
                furniture = self.furnitureList[index]
                self.selectedFurniture, self.count = furniture, 1
                break
            else: self.selectedFurniture = None
        if (self.editMode == False and self.createStatus == False
            and len(self.Ezzies) > 0 and self.count == 1): #carry
            self.drawMotion(event.x, event.y, self.selectedEzzy)

        #select action for Ezzy
        if self.selectedFurniture == None:
            for i in xrange(len(self.Ezzies)):
                ezzy = self.Ezzies[i]
                x_r, y_r, x, y = 90, 100, ezzy.x, ezzy.y
                if (event.x > x-x_r and event.x < x+x_r and
                    event.y >y-y_r and event.y < y+y_r):
                    self.ezzyIndex, self.selectedEzzy = i, ezzy
                    break

    def checkSelection(self, event):
        #Checks the selected furniture and replenishes stats based on action
        ezzy = self.selectedEzzy
        x, y, x_r, y_r = 685, 585, 30, 15
        if (event.x > x-x_r and event.x < x+x_r and
            event.y > y-y_r and event.y < y+y_r):
            self.doAnimation = True
            if (self.selectedFurniture.furnIndex == 2 or
                self.selectedFurniture.furnIndex == 0): ezzy.energy = 20
            elif (self.selectedFurniture.furnIndex == 1):
                ezzy.bladder = 20
                ezzy.clean -= 5
            elif (self.selectedFurniture.furnIndex == 3 or
                  self.selectedFurniture.furnIndex == 4):
                ezzy.fun = 20
                ezzy.energy -= 2
            elif (self.selectedFurniture.furnIndex == 5): ezzy.clean = 20
            elif (self.selectedFurniture.furnIndex == 7): ezzy.hunger = 20
        self.count = 0
            
    def Animation(self, furniture):
        #Action text that appears at the bottom right block
        x, y = 685, 585
        if furniture.furnIndex == 2: #bed
            self.selectText = PhotoImage(file="texts.sleep.gif")
            self.selectTextActive = PhotoImage(file="texts.sleep.active.gif")
            self.canvas.create_image(x, y, image=self.selectText,
                                     active=self.selectTextActive)
        elif furniture.furnIndex == 0: #chair
            self.selectText = PhotoImage(file="texts.sit.gif")
            self.selectTextActive = PhotoImage(file="texts.sit.active.gif")
            self.canvas.create_image(x, y, image=self.selectText,
                                     active=self.selectTextActive)
        elif furniture.furnIndex == 7: #fridge
            self.selectText = PhotoImage(file="texts.eat.gif")
            self.selectTextActive = PhotoImage(file="texts.eat.active.gif")
            self.canvas.create_image(x, y, image=self.selectText,
                                     active=self.selectTextActive)
        elif furniture.furnIndex in [1,3,4,5]: #the rest
            self.selectText = PhotoImage(file="texts.use.gif")
            self.selectTextActive = PhotoImage(file="texts.use.active.gif")
            self.canvas.create_image(x, y, image=self.selectText,
                                     active=self.selectTextActive)

    def chooseFurniture(self, event):
        #select furniture index based on click
        if self.selector == True:
            if event.y > 530 and event.y < 580 and self.money-self.cost >= 0:
                if (event.x > 425 and event.x < 550): #Chair
                    self.selectorIndex, self.selectorCount = 0, 2
                    self.x_r, self.y_r = 50, 50
                    self.selector = False
                elif (event.x > 550 and event.x < 675): #Toilet
                    self.selectorIndex, self.selectorCount = 1, 2
                    self.x_r, self.y_r = 50, 50
                    self.selector = False
                elif (event.x > 675 and event.x < 800): #Bed
                    self.selectorIndex, self.selectorCount = 2, 2
                    self.x_r, self.y_r = 85, 75
                    self.selector = False
                elif (event.x > 800 and event.x < 925): #TV
                    self.selectorIndex, self.selectorCount = 3, 2
                    self.x_r, self.y_r = 60, 50
                    self.selector = False
            elif event.y > 580 and event.y < 630:
                if (event.x > 425 and event.x < 550): #Computer
                    self.selectorIndex, self.selectorCount = 4, 2
                    self.x_r, self.y_r = 60, 50
                    self.selector = False
                elif (event.x > 550 and event.x < 675): #Shower
                    self.selectorIndex, self.selectorCount = 5, 2
                    self.x_r, self.y_r = 60, 100
                    self.selector = False
                elif (event.x > 675 and event.x < 800): #Table
                    self.selectorIndex, self.selectorCount = 6, 2
                    self.x_r, self.y_r = 85, 750
                    self.selector = False
                elif (event.x > 800 and event.x < 925): #Fridge
                    self.selectorIndex, self.selectorCount = 7, 2
                    self.x_r, self.y_r = 60, 100
                    self.selector = False
            else: self.selectorCount = 0
            if self.selector == False: self.money -= self.cost
            
    def placeFurniture(self, event):
        #place furniture on map
        yMax =self.middleX
        if (self.selector == False and self.selectorCount == 2 and
            event.y < yMax):
            self.selectorCount = 0
            furniture = Furniture(self.selectorIndex, event.x, event.y)
            self.furnitureList.append(furniture)
            self.space.append((event.x, event.y, self.x_r, self.y_r,
                          len(self.furnitureList)-1))
            self.selectorIndex = None
            
    def onMouseMotion(self, event): ########### MOUSE MOTION ###########
        #Carry out actions based on mouse motion
        draw, self.randomTextIndex = False, random.randint(0,1)
        if self.park and self.parkPlay: self.motionPark(event) #mini-game
        else:
            #self.selector only turns on when the mouse is in the game window
            if (self.selector == True and event.y < self.height and
                event.y > self.gameHeight):
                self.selector = True
            else: self.selector = False
            
            #personality/mood actions will occur based on where the mouse is
            if self.personalityAction != None:
                self.moodCount += 1
                ezzy = self.moodyEzzy
                if self.moodCount == 100:
                    self.moodCount, self.personalityAction = 0, None
                self.personalityHelper(ezzy, event)

    def motionPark(self, event):
        #In Pedestal Park mini-game:
        #Adds money every time the mouse is hovered over the human
        if (event.x > self.humanX-self.humanR and
            event.x < self.humanX+self.humanR and
            event.y > self.humanY-self.humanR and
            event.y < self.humanY+self.humanR):
            self.money += .1

    def personalityHelper(self, ezzy, event):
        delay, text_x, text_y = 20, 950, 500
        #Based on the personality of the ezzy that is having the mood swing:
        if self.personalityAction == "rebel":
            #Rebels will move away from the mouse and bounce around
            if self.moodCount % delay == 0: #delays the movements
                randomText = ["No NO No Noooo NOOOO",
                            "Whatever, I do what I want"]
                if self.moodText == 1:
                    self.moodText = 0
                    self.canvas.create_text(text_x, text_y, anchor = "se",
                fill = "floral white", font="Helvetica 20",
                text= "%s" % randomText[self.randomTextIndex])
                if ezzy.x == 0: self.drawMotion (self.width, ezzy.y, ezzy)
                elif ezzy.x == self.width: self.drawMotion (0, ezzy.y, ezzy)
                elif ezzy.y == 0: self.drawMotion (ezzy.x, self.ezzyH, ezzy)
                elif ezzy.y == self.ezzyH: self.drawMotion (ezzy.x, 0, ezzy)
                else: self.drawMotion(ezzy.x+event.x, ezzy.y+event.y, ezzy)
        elif self.personalityAction == "nerd":
            #Nerds will move towards the mouse and follow it around
            if self.moodCount % delay == 0: 
                randomText = ["Oh boy! What do you wanna do today?!",
                "According to my calculations, you're my friend"]
                self.canvas.create_text(text_x, text_y, anchor = "se",
                fill = "floral white", font="Helvetica 20",
                text= "%s" % randomText[self.randomTextIndex])
                self.drawMotion(event.x, event.y, ezzy)
            
    def onTimerFired(self): ########### TIMER FIRED ###########
        #Every second, execute onTimerFired
        
        if self.Ezzies != [] and self.town == False: #if there are Ezzies:
            for i in xrange(len(self.Ezzies)):
                #for each ezzy: check needs, change moods, age, and give
                #them automatic commands based on probability
                ezzy = self.Ezzies[i]
                self.timerEzzy(ezzy)
                if self.selectedFurniture == None: self.randomMove(ezzy)
                ezzy.automaticCare()
                if ezzy.doAutomatic == True:
                    ezzy.doAutomatic = False
                    if self.findFurniture(ezzy) == True: self.careAction(ezzy)
                    else: ezzy.careIndex = None     
                if ezzy.moodSwing() == True:
                    self.moodyEzzy = ezzy
                    if ezzy.Rebel == True:
                        self.personalityAction, ezzy.Rebel = "rebel", False
                    elif ezzy.Nerd == True:
                        self.personalityAction, ezzy.Nerd = "nerd", False
        if self.twerkPlay: self.twerkTimer -= 1

    def timerEzzy(self, ezzy):
        #For each ezzy, check all needed methods
        ezzy.counter = (ezzy.counter + 1) % self.needtimeMax
        ezzy.checkNeeds()
        ezzy.changeMood()
        ezzy.ageEzzy()
        ezzy.checkDead()
        
    def gameTimerFired(self):
        #Runs only when Pedestal Park is playing: Has faster clock
        startCounter, randRangeA, randRangeB = 10, -100, 100
        if self.parkPlay:
            self.counter += 1
            if self.counter == startCounter:
                #since timer is 100 ms: parkTimer decreases by 1 each second
                self.parkTimer -= 1
                self.counter = 0

            #move the ball around randomly and have wrap arround
            if self.humanX == 0:
                delta = random.randint(randRangeA, randRangeB) 
                if self.humanX + delta > 0:
                    self.humanX += delta
            if self.humanX > 0 and self.humanX < self.width:
                self.humanX = (self.humanX + self.deltaX) % self.width
            else: self.deltaX = random.randint(randRangeA, randRangeB) 
            if self.humanY > 0 and self.humanY < self.gameHeight:
                self.humanY = (self.humanY + self.deltaY) % self.gameHeight
            else: self.deltaY = random.randint(randRangeA, randRangeB)

            #draw the human circle
            self.canvas.create_oval(self.humanX-self.humanR,
            self.humanY-self.humanR, self.humanX+self.humanR,
            self.humanY+self.humanR, fill="white", width=2)
            
    def findFurniture(self, ezzy):
        #searches the furniture list for a fitting furniture
        #used for automatic Ezzy actions
        for furn in self.furnitureList:
            if furn.furnIndex == ezzy.careIndex:
                #found furniture in room that satisfies care requirement
                self.selectedFurniture = furn
                self.automaticEzzy = ezzy
                self.doAnimation = True
                return True
        return False

    def careAction(self, ezzy):
        #used for automatic Ezzy actions -> Finds furniture and keeps needs up
        self.drawMotion(self.selectedFurniture.x,self.selectedFurniture.y,ezzy)
        if (self.selectedFurniture.furnIndex == 2 or
                self.selectedFurniture.furnIndex == 0): ezzy.energy = 20
        elif (self.selectedFurniture.furnIndex == 1):
                ezzy.bladder = 20
                ezzy.clean -= 5
        elif (self.selectedFurniture.furnIndex == 3 or
                  self.selectedFurniture.furnIndex == 4):
                ezzy.fun = 20
                ezzy.energy -= 2
        elif (self.selectedFurniture.furnIndex == 5): ezzy.clean = 20
        elif (self.selectedFurniture.furnIndex == 7): ezzy.hunger = 20
        ezzy.careIndex, ezzy.doAutomatic = None, False

    def randomMove(self, ezzy):
        #Have Ezzies move randomly across the screen
        if random.randint(0,20) == 10:
            move_x = random.randint(0,self.width)
            move_y = random.randint(0,self.ezzyH)
            self.drawMotion(move_x, move_y, ezzy)

    def drawEditMode(self):
        #Draws a green rectangle around the screen when edit mode is on
        startXY = 3
        self.canvas.create_rectangle(startXY, startXY, self.width,
                                     self.gameHeight,outline="green",width=2)

    def drawMenuScreen(self):
        #Draws the menu screen texts
        start, yFactor = 180, 70
        if self.menuCount != 1:
            self.menuScreen = PhotoImage(file="menu.display.gif")
            self.canvas.create_image(self.width/2, self.middleY,
                                     image=self.menuScreen)
            self.canvas.create_text(self.width/2, start, text = "About",
                                    font = "Helvetica 35", fill = "PaleGreen1",
                                    activefill = "PaleGreen4")
            self.canvas.create_text(self.width/2, start+yFactor, text = "Ezzy?",
                                    font = "Helvetica 35",
                                    fill = "SkyBlue1", activefill = "SkyBlue4")
            self.canvas.create_text(self.width/2, start+yFactor*2,
                                    text = "Help", font = "Helvetica 35",
                                    fill = "bisque", activefill = "bisque4")
            self.canvas.create_text(self.width/2, start+yFactor*3,fill="salmon",
                                    text = "Save", font = "Helvetica 35", 
                                    activefill = "salmon4")
            self.canvas.create_text(self.width/2, start+yFactor*4,
                                    text = "Load", activefill = "purple4",
                                    font = "Helvetica 35", fill = "purple")
        else: self.canvas.create_image(self.width/2, self.middleY,
                                       image=self.menuScreen)   
    
    def redrawAll(self): ########### REDRAW ALL ###########
        #Draws everything based on conditions
        self.redrawAllHelper()
        if self.menuStatus == True: self.drawMenuScreen()
        elif self.createStatus == True: self.drawCreateMode()
        elif self.town == True: self.drawTown()
        elif self.twerk or self.park: self.runGames()
        else: #when not displaying the menu screen, display the game
            self.floor = PhotoImage(file="floor.gif")
            self.canvas.create_image(self.middleX, self.middleY,
                                     image=self.floor)
            for i in xrange(len(self.furnitureList)):
                self.furnitureList[i].drawFurniture(self.canvas)
            for i in xrange(len(self.Ezzies)):
                self.Ezzies[i].drawEzzy(self.canvas)
            self.condDrawHelper()
            if len(self.Ezzies) > 0:
                self.canvas.create_text(950,20, fill="floral white",
                text=self.selectedEzzy.name, font="Helvetica 20",anchor="ne")
                self.drawStatusBars()

    def redrawAllHelper(self):
        #Continuation of redrawAll
        self.canvas.delete(ALL)
        if self.moodText == 0: self.moodText = 1
        self.canvas.create_rectangle(0,self.gameHeight,self.width,700,fill="white")
        self.drawCreateEzzy()
        self.drawMenu()
        self.drawShop()

    def condDrawHelper(self):
        #Continuation of redrawAll
        if (self.selectedFurniture != None and self.count==1 and
            self.automaticEzzy == None):
            self.Animation(self.selectedFurniture)
        if self.selector == True: self.drawMenus()
        if self.help == True: self.drawHelp()
        if self.editMode == True: self.drawEditMode()
        if (self.doAnimation == True and self.selectedFurniture != None):
            #draw furniture animation for Ezzies
            if self.automaticEzzy != None:
                ezzy, self.automaticEzzy = self.automaticEzzy, None
            else: ezzy = self.selectedEzzy                    
            self.doAnimations(self.selectedFurniture.furnIndex, ezzy)


    def runGames(self): #Run mini-games
        if self.twerk == True: self.twerking()
        elif self.park == True: self.parking()
        
    def initializeTwerk(self): #initialize vairbles for Get Twerk mini-game
        if self.advance == True:
            self.twerkTimer = 25
            self.advance = False
            self.userInput = ""
            characterCount = self.currentLevel*3
            self.twerkText = self.generateRandomReports(characterCount)

    def twerking(self): #Get Twerk mini-game
        self.initializeTwerk()
        self.drawTwerk()
        if self.twerkPlay == True:
            if self.currentLevel <= self.maxLevel:
                if self.userInput == self.twerkText: #advance a level
                        self.currentLevel += 1
                        self.advance = True
                elif self.twerkTimer == 0: #out of time
                    self.twerkPlay = False
                    self.twerkLose = True
            else:
                self.twerkPlay, self.twerkWin = False, True
            self.canvas.create_text(self.middleX, 300, font= "Helvetica 25",
                        text=self.userInput,fill="light sky blue")
            self.canvas.create_text(self.middleX, 210, font= "Helvetica 25",
                        text=self.twerkText,fill="dark slate blue")
            self.canvas.create_text(400, 450,font=" Helvetica 25",
                        text=self.twerkTimer,fill="white")
            self.canvas.create_text(400, 50, font="Helvetica 25",
                        text=self.currentLevel,fill="white")
                    
    def generateRandomReports(self, letterCount): #Get Twerk reports/challenges
        text = ""
        for letter in xrange(letterCount):
            temp = random.randint(33,125)
            text += chr(temp)
        return text
        
    def drawTwerk(self):
        x1, x2, y = 200, 840, 360
        #Draw Get Twerk animations (instructions, start, and game play)
        if self.twerkInstructions == True:
            self.drawGame = PhotoImage(file="twerk.instructions.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
        elif self.twerkStart == True:
            self.drawGame = PhotoImage(file="twerk.start.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
        elif self.twerkPlay == True:
            self.drawGame = PhotoImage(file="twerk.play.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
        elif self.twerkWin or self.twerkLose:
            income = 0
            for i in xrange(self.currentLevel): income += 3*i
            self.money += income
            if self.twerkWin: self.drawEnd = PhotoImage(file="twerk.win.gif")
            elif self.twerkLose:self.drawEnd=PhotoImage(file="twerk.lose.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawEnd)
            self.canvas.create_text(x1, y, text=income, font="Helvetica 25")
            self.canvas.create_text(x2, y,text=self.money,font="Helvetica 25")
            self.canvas.update()
            self.canvas.after(6000)
            self.twerk = False
        
    def parking(self): #Pedestal Park mini-game
        self.drawPark()
        if self.parkTimer == 0:
            self.parkOver = True
            self.parkPlay = False
        #Randomly change the direction of the moving human
        if random.randint(0,10) == 0: self.deltaX *= -1
        elif random.randint(0, 10) == 10: self.deltaY *= -1
        
    def drawPark(self):
        #Draw the mini-game Pedestal Park
        x, y1, y2 = 10, 10, 515
        income = str(int(self.money - self.previousMoney))
        if self.parkInstructions == True:
            self.drawGame = PhotoImage(file="park.instructions.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
        elif self.parkStart == True:
            self.drawGame = PhotoImage(file="park.start.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
        elif self.parkPlay == True:
            self.drawGame = PhotoImage(file="park.play.gif")
            self.canvas.create_image(self.middleX, self.middleY, image=self.drawGame)
            self.canvas.create_text(x, y1, text="Time: " + str(self.parkTimer),
                            fill="white", font="Helvetica 25", anchor="nw")
            self.canvas.create_text(x, y2, text="Score: " + income,
                            fill="white", font="Helvetica 25", anchor="sw")
        elif self.parkOver == True: self.parkWinLoseHelper(income)

    def parkWinLoseHelper(self, income):
        #Pedestal Park win/lose screens
        x, y1, y2, timeDelay = 770, 300, 440, 6000
        self.money = int(self.money)
        self.drawEnd = PhotoImage(file="park.end.gif")
        self.canvas.create_image(self.middleX, self.middleY, image=self.drawEnd)
        self.canvas.create_text(x, y1, text=income, font="Helvetica 25")
        self.canvas.create_text(x, y2,text=self.money,font="Helvetica 25")
        self.canvas.update()
        self.canvas.after(timeDelay)
        self.park, self.gameFired, self.timerFired = False, False, True
        
    def doAnimations(self, index, ezzy):
        #Create animation for Ezzy when it uses the bathroom
        #Depending on which personality/age the Ezzy is, the appropriate
        #animation will be selected and implemented
        self.selectedEzzy.drawOn = False
        ezzyType = (ezzy.personality, ezzy.ageIndex)
        if ezzyType == (1, None): ezzyType = None #Normal Ezzy
        if index == 0:
            self.selectedFurniture.chairAnimation(self.canvas, ezzyType)
        elif index == 1:
            self.selectedFurniture.toiletAnimation(self.canvas, ezzyType)
        elif index == 2:
            self.selectedFurniture.bedAnimation(self.canvas, ezzyType)
        elif index == 3:
            self.selectedFurniture.televisionAnimation(self.canvas, ezzyType)
        elif index == 4:
            self.selectedFurniture.computerAnimation(self.canvas, ezzyType)
        elif index == 5:
            self.selectedFurniture.showerAnimation(self.canvas, ezzyType)
        elif index == 7:
            self.selectedFurniture.fridgeAnimation(self.canvas, ezzyType)
        self.selectedFurniture = None
        self.doAnimation = False
        self.selectedEzzy.drawOn = True
        
    def initiateMenus(self):
        #Initiates the menu text bar for furniture in the Shop
        self.menuFiles = []
        self.menuActiveFiles = []
        self.furniture = ["texts.chair.gif","texts.toilet.gif",
                          "texts.bed.gif","texts.television.gif",
                          "texts.computer.gif","texts.shower.gif",
                          "texts.table.gif","texts.fridge.gif"]
        for i in xrange(len(self.furniture)):
            self.menuFiles.append(PhotoImage(file=self.furniture[i]))
            activeText = self.furniture[i][0:-4] + ".active.gif"
            self.menuActiveFiles.append(PhotoImage(file=activeText))

    def displayCreate(self):
        #Creates display of Create Ezzy screen
        self.entryName = ""
        self.displayCreateBG = True
        self.displayCreateName = True
        self.selectedAge = None

    def drawCreateMode(self):
        #Launches the create Ezzy mode
        if self.displayCreateBG == True:
            self.drawCreateModeHelper()
        if self.displayCreateName == True:
            self.createNAME = PhotoImage(file="create.name.gif")
            y1, y2 = 390, 420
            self.canvas.create_image(self.middleX, y1, image=self.createNAME)
            self.canvas.create_text(self.middleX, y2, font = "Helvetica 16",
                                    text="%s" % self.entryName)
        if self.pickPersonality == True: self.drawpickPersonality()
        if self.selectAge == True: self.drawselectAge()

    def drawCreateModeHelper(self):
        #Helper of Draw Create Mode: Creates background and other UI for mode
        self.createBG = PhotoImage(file="create.background.gif")
        self.canvas.create_image(self.middleX, self.middleY,
                                image=self.createBG)
        if self.selectedPersonality != None:
            index = self.selectedPersonality
            self.createEzzy = PhotoImage(file=self.personalityList[index])
        else: self.createEzzy = PhotoImage(file="ezzy.1.1.gif")
        if self.createComplete == True:
            self.createEzzy = PhotoImage(file="ezzy.1.gif")
            self.canvas.create_image(self.middleX, self.middleY,
                                    image=self.createEzzy)
            self.canvas.update()
            self.canvas.after(self.middleX)
            self.createComplete = False
        else:
            self.canvas.create_image(self.middleX, self.middleY,
                                    image=self.createEzzy)
            
    def drawselectAge(self):
        #Draw the select age screen
        if self.selectedPersonality == 1:
            self.selectAgeHelper()
            return None
        self.tempFile = PhotoImage(file="create.age.gif")
        y, y_mid, x1, x2 = 360, 420, 170, 830
        self.canvas.create_image(self.middleX, y_mid, image=self.tempFile)
        if self.selectedPersonality == 0: #rebel
            self.tempFile1 = PhotoImage(file = "ezzy.rebel.young.1.gif")
            self.tempFileActive1 = PhotoImage(file = "ezzy.rebel.young.2.gif")
            self.tempFile2 = PhotoImage(file = "ezzy.rebel.old.2.gif")
            self.tempFileActive2 = PhotoImage(file = "ezzy.rebel.old.1.gif")
        else: #nerd
            self.tempFile1 = PhotoImage(file = "ezzy.nerd.young.2.gif")
            self.tempFileActive1 = PhotoImage(file = "ezzy.nerd.young.1.gif")
            self.tempFile2 = PhotoImage(file = "ezzy.nerd.old.2.gif")
            self.tempFileActive2 = PhotoImage(file = "ezzy.nerd.old.1.gif")
        self.canvas.create_image(x1, y, image=self.tempFile1,
                                     active = self.tempFileActive1)
        self.canvas.create_image(x2, y, image=self.tempFile2,
                                     active = self.tempFileActive2)

    def selectAgeHelper(self):
        #Helper of create age screen
        self.selectAge = False
        self.createObj()
        self.selectedEzzy = self.Ezzies[-1]
        self.displayCreateBG = False
        self.createStatus = False

    def drawpickPersonality(self):
        #Helper of create age screen
        length, y = 250, 390
        self.tempFile1 = PhotoImage(file = "ezzy.rebel.gif")
        self.tempActiveFile1 = PhotoImage(file = "ezzy.rebel.active.gif")
        self.canvas.create_image(length, y, image=self.tempFile1,
                                     active=self.tempActiveFile1)
        self.tempFile2 = PhotoImage(file = "ezzy.normal.gif")
        self.tempActiveFile2 = PhotoImage(file = "ezzy.normal.active.gif")
        self.canvas.create_image(self.middleX, y, image=self.tempFile2,
                                     active=self.tempActiveFile2)
        self.tempFile3 = PhotoImage(file = "ezzy.nerd.gif")
        self.tempActiveFile3 = PhotoImage(file = "ezzy.nerd.active.gif")
        self.canvas.create_image(self.middleX+length, y, image=self.tempFile3,
                                     active=self.tempActiveFile3)
        
    def drawMenus(self):
        #Draw menu texts on the menu bar at the bottom
        x = 425
        y = 530
        y2 = 580
        half, length = 4, 125
        for i in xrange(len(self.furniture)):
            if i >= half: y = y2
            self.canvas.create_image(x+(i%half)*length, y,
                                         image=self.menuFiles[i], anchor = "nw",
                                         active=self.menuActiveFiles[i])

    def drawStatusBars(self):
        #Display the status of the current ezzy selected
        if len(self.Ezzies) != 0:
            ezzy = self.selectedEzzy
            radius = 25
            numNeeds = 5
            needsList = [ezzy.bladder, ezzy.fun, ezzy.energy,
                         ezzy.clean, ezzy.hunger]
            textList = ["Bladder", "Fun", "Energy", "Clean", "Hunger"]
            for i in xrange(numNeeds):
                if needsList[i] <= 0: tempRadius = 0
                else: tempRadius = radius
                self.canvas.create_rectangle(tempRadius, radius+i*radius, 
                                             tempRadius*2+needsList[i]*numNeeds,
                                             (radius*2+i*radius), fill="green")
                self.canvas.create_text(85, 10+radius+i*radius, text=textList[i])
                self.canvas.create_rectangle(radius,radius+i*radius, 
                                             radius*2+100,
                                             radius*2+i*radius, width=2)
        #Also display the user's bank account (how much money they have)
        self.canvas.create_text(radius-numNeeds, self.middleX + radius,
                                anchor = "sw", font= "Helvetica 15",
                                text=self.money, fill="forest green")
        
    def drawCreateEzzy(self):
        #draw create button
        self.button = PhotoImage(file="create.gif")
        self.buttonactive = PhotoImage(file="createactive.gif")
        self.canvas.create_image(self.barX,self.height, anchor = "sw",
                                 image = self.button,
                                 active = self.buttonactive)

    def drawMenu(self):
        #draw menu button
        self.menu = PhotoImage(file="menu.gif")
        self.menuactive = PhotoImage(file="menuactive.gif")
        self.canvas.create_image(0, self.height, anchor='sw', image=self.menu, 
                                 active=self.menuactive)

    def drawShop(self):
        #draw shop button
        self.shop = PhotoImage(file="shop.gif")
        self.shopactive = PhotoImage(file="shopactive.gif")
        self.canvas.create_image(self.barX*2, self.height, anchor='sw',
                                 image=self.shop,
                                 active=self.shopactive)

    def drawMotion(self, x, y, ezzy):
        #Draws the up and down movement of Ezzy, as well as moves Ezzy
        ezzy.moveEzzy(x, y)
        for i in xrange(ezzy.stepFactor):
            ezzy.x += ezzy.xfactor
            ezzy.y += ezzy.yfactor
            if ezzy.personality == 1 or ezzy.ageIndex == 0:
                if ezzy.motion == 0: ezzy.motion = 1
                elif ezzy.motion == 1: ezzy.motion = 0
            elif ezzy.personality == 0 or ezzy.personality == 2:
                if ezzy.motion == 0: ezzy.motion = 1
                elif ezzy.motion == 1: ezzy.motion = 2
                elif ezzy.motion == 2: ezzy.motion = 1
            ezzy.drawEzzy(self.canvas)
            self.canvas.after(150)
            self.canvas.update()
            ezzy.energy -= 0.01 # Lose energy each movement
        ezzy.motion = 0 #Always ends on ezzy.motion = 0 (lands on ground)

    def drawTown(self):
        #Draw the town screen
        x1, x2, y = 150, 850, 290
        self.townPic = PhotoImage(file="town.gif")
        self.twerkPic = PhotoImage(file="twerk.gif")
        self.twerkPicActive = PhotoImage(file="twerk.active.gif")
        self.parkPic = PhotoImage(file="park.gif")
        self.parkPicActive = PhotoImage(file="park.active.gif")
        self.canvas.create_image(self.width/2, self.gameHeight/2, image=self.townPic)
        self.canvas.create_image(x1, y, image = self.twerkPic,
                                 active = self.twerkPicActive)
        self.canvas.create_image(x2, y, image = self.parkPic,
                                 active = self.parkPicActive)

class Furniture(object):
    
    def __init__(self, index, x, y, ezzyType=None):
        #Initializes Furniture Conditions
        self.furnIndex = index
        self.furnFile = None
        self.x, self.y = x, y
        self.selectFurniture()
        
    def selectFurniture(self):
        #List of furnitures to select from
        self.furniture = ["chair.gif","toilet.gif",
                          "bed.gif","television.gif",
                          "computer.gif","shower.1.1.gif",
                          "table.gif","fridge.gif"]
        self.furnFile = self.furniture[self.furnIndex]
        
    def drawFurniture(self, canvas):
        #Create image and draw furniture
        self.furniturePic = PhotoImage(file="%s" % self.furnFile)
        if self.furnIndex == 7: #if fridge (that needs an active file)
            self.furnitureActive = PhotoImage(file="fridge.active.gif")
            canvas.create_image(self.x, self.y, image=self.furniturePic,
                                active=self.furnitureActive)
        else:
            canvas.create_image(self.x, self.y, image=self.furniturePic)

    def bedAnimation(self, canvas, ezzyType=None):
        #Draws the bed animation for each type of Ezzy
        if ezzyType == None:
            furnitureAnim = ["bed.1.2.gif", "bed.1.3.gif"]
            self.drawInitialBedAnimation(canvas)
            loopCount = 10
        else:
            if ezzyType[0] == 0: # Rebel
                if ezzyType[1] == 0: # Young
                    furnitureAnim = ["bed.1.rebel.gif", "bed.1.1.rebel.gif"]
                elif ezzyType[1] == 1: # Old
                    furnitureAnim = ["bed.1.rebel.old.gif",
                                     "bed.1.1.rebel.old.gif"]
            elif ezzyType[0] == 2: # Nerd
                if ezzyType[1] == 0: # Young
                    furnitureAnim = ["bed.1.nerd.gif", "bed.1.1.nerd.gif"]
                elif ezzyType[1] == 1: # Old
                    furnitureAnim = ["bed.1.nerd.old.gif",
                                     "bed.1.1.nerd.old.gif"]
            loopCount = 15 if ezzyType[1] == 1 else 10 #the old sleep longer
        for i in xrange(loopCount):
            index = i%2
            self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
            canvas.create_image(self.x, self.y, image=self.tempPicture)            
            canvas.update()
            canvas.after(1000)

    def drawInitialBedAnimation(self, canvas):
        #Add-on to Bed Animation
        self.tempPicture = PhotoImage(file="bed.1.gif")
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(2000)
        self.tempPicture = PhotoImage(file="bed.1.1.gif")
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(2000)
        canvas.update()

    def televisionAnimation(self, canvas, ezzyType=None):
        #Draws the TV animation for each type of Ezzy
        if ezzyType == None:
            self.tempPicture = PhotoImage(file="television.1.gif")
        elif ezzyType[0] == 0:
            self.tempPicture = PhotoImage(file="television.1.rebel.gif")
        elif ezzyType[0] == 2:
            self.tempPicture = PhotoImage(file="television.1.nerd.gif")
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(5000)
        
    def computerAnimation(self, canvas, ezzyType=None):
        #Draws the computer animation for each type of Ezzy
        if ezzyType == None:
            furnitureAnim = ["computer.1.1.gif", "computer.1.2.gif"]
            self.tempPicture = PhotoImage(file="computer.1.gif")
            canvas.create_image(self.x, self.y, image=self.tempPicture)
            canvas.update()
            canvas.after(3000)
            for i in xrange(5):
                index = i%2
                self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
                canvas.create_image(self.x, self.y, image=self.tempPicture)
                canvas.update()
                canvas.after(2000)
        else:
            if ezzyType[0] == 0: # Rebel
                    self.tempPicture = PhotoImage(file="computer.1.rebel.gif")
            elif ezzyType[0] == 2: # Nerd
                    self.tempPicture = PhotoImage(file="computer.1.nerd.gif")
            time = 10 if ezzyType[0] == 0 else 15
            #nerds stay on computers longer
            canvas.create_image(self.x, self.y, image=self.tempPicture)
            canvas.update()
            canvas.after(time*1000)

    def showerAnimation(self, canvas, ezzyType=None):
        #Draws the shower animation for each type of Ezzy
        furnitureAnim = ["shower.1.1.gif", "shower.1.2.gif"]
        self.showerAnimationHelper(canvas, ezzyType)
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(2000)    
        for i in xrange(10):
            index = i%2
            self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
            canvas.create_image(self.x, self.y, image=self.tempPicture)
            canvas.update()
            canvas.after(500)
        canvas.create_image(self.x, self.y, image=self.tempPictureEnd)
        canvas.update()
        canvas.after(2000)

    def showerAnimationHelper(self, canvas, ezzyType):
        #Add-on to the shower animation
        if ezzyType == None:
            self.tempPicture = PhotoImage(file="shower.gif")
            self.tempPictureEnd = PhotoImage(file="shower.1.gif")
        else:
            if ezzyType[0] == 0: # Rebel
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="shower.rebel.gif")
                    self.tempPictureEnd = PhotoImage(file="shower.1.rebel.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture = PhotoImage(file="shower.rebel.old.gif")
                    self.tempPictureEnd=PhotoImage(file="shower.1.rebel.old.gif")
            elif ezzyType[0] == 2: # Nerd
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="shower.nerd.gif")
                    self.tempPictureEnd = PhotoImage(file="shower.1.nerd.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture = PhotoImage(file="shower.nerd.old.gif")
                    self.tempPictureEnd=PhotoImage(file="shower.1.nerd.old.gif")
        
    def toiletAnimation(self, canvas, ezzyType=None):
        #Draws the toilet animation for each type of Ezzy
        if ezzyType == None or ezzyType[0] == 0:
            if ezzyType == None:
                self.tempPicture = PhotoImage(file="toilet.1.gif")
                furnitureAnim = ["toilet.1.1.gif", "toilet.1.2.gif"]
                self.tempPictureEnd = PhotoImage(file="toilet.1.3.gif")
            else:
                if ezzyType[0] == 0: # Rebel
                    if ezzyType[1] == 0: # Young
                        self.tempPicture = PhotoImage(file="toilet.1.rebel.gif")
                        furnitureAnim = ["toilet.1.1.rebel.gif",
                                         "toilet.1.2.rebel.gif"]
                        self.tempPictureEnd=PhotoImage(file="toilet.1.3.rebel.gif")
                    elif ezzyType[1] == 1: # Old
                        self.tempPicture = PhotoImage(file="toilet.1.rebel.old.gif")
                        furnitureAnim = ["toilet.1.1.rebel.old.gif",
                                         "toilet.1.2.rebel.old.gif"]
                        self.tempPictureEnd=PhotoImage(file="toilet.1.3.rebel.old.gif")
            self.toiletAnimationHelper(canvas, furnitureAnim)
        else:
            if ezzyType[1] == 0: # Young
                furnitureAnim = ["toilet.1.nerd.gif","toilet.1.1.nerd.gif"]
            elif ezzyType[1] == 1: # Old
                furnitureAnim = ["toilet.1.nerd.old.gif","toilet.1.1.nerd.old.gif"]
            for i in xrange(4):
                index = i%2
                self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
                canvas.create_image(self.x, self.y, image=self.tempPicture)
                canvas.update()
                canvas.after(3000)
        
    def toiletAnimationHelper(self, canvas, furnitureAnim):
        #Add-on to the toilet animation
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(2000)
        for i in xrange(3):
            index = i%2
            self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
            canvas.create_image(self.x, self.y, image=self.tempPicture)
            canvas.update()
            canvas.after(3000)
        canvas.create_image(self.x, self.y, image=self.tempPictureEnd)
        canvas.update()
        canvas.after(2000)
        
    def fridgeAnimation(self, canvas, ezzyType=None):
        #Draws the fridge animation for each type of Ezzy
        if ezzyType == None: self.tempPicture=PhotoImage(file="fridge.1.2.gif")
        else: 
            if ezzyType[0] == 0: # Rebel
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="fridge.1.2.rebel.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture=PhotoImage(file="fridge.1.2.rebel.old.gif")
            elif ezzyType[0] == 2: # Nerd
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="fridge.1.2.nerd.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture=PhotoImage(file="fridge.1.2.nerd.old.gif")
        canvas.create_image(self.x, self.y, image=self.tempPicture)
        canvas.update()
        canvas.after(2500)
        furnitureAnim = ["fridge.1.gif", "fridge.1.1.gif"]
        for i in xrange(10):
            index = i%2
            self.tempPicture = PhotoImage(file="%s" % furnitureAnim[index])
            canvas.create_image(self.x,self.y,image=self.tempPicture)
            canvas.update()
            canvas.after(1000)

    def chairAnimation(self, canvas, ezzyType=None):
        #Draws the chair animation for each type of Ezzy
        if ezzyType == None:
            self.tempPicture = PhotoImage(file="chair.1.gif")
            time = 5
        else:
            if ezzyType[0] == 0: # Rebel
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="chair.1.rebel.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture = PhotoImage(file="chair.1.rebel.old.gif")
            elif ezzyType[0] == 2: # Nerd
                if ezzyType[1] == 0: # Young
                    self.tempPicture = PhotoImage(file="chair.1.nerd.gif")
                elif ezzyType[1] == 1: # Old
                    self.tempPicture = PhotoImage(file="chair.1.nerd.old.gif")
            time = 7 if ezzyType[1] == 1 else 5
        canvas.create_image(self.x,self.y,image=self.tempPicture)
        canvas.update()
        canvas.after(time*1000)
        
class Ezzy(object):
    
    def __init__(self, x, y, name, personality, age):
        #Initializes Ezzy conditions
        self.personality = personality
        self.name = name
        self.age, self.ageIndex = age, 0
        if self.age == 1: self.age, self.ageIndex = 50, 1
        if self.age == None: self.ageIndex = None
        self.initiateMoods(personality)
        self.initiateStep()
        self.moodindex, self.counter = 0, 0
        self.radiusX, self.radiusY = 220, 70
        self.x, self.y = x/2, y/2
        self.bladder, self.fun, self.energy = 20, 20, 20
        self.clean, self.hunger, self.happiness = 20, 20, 100
        self.doAutomatic, self.drawOn, self.careIndex = False, True, None
        self.motion = 0 #Alternates between 0 and 1 for normal; 1 and 2 for R/N
        self.Rebel, self.Nerd = None, None
        if self.personality == 0: self.Rebel = False
        elif self.personality == 2: self.Nerd = False
        self.dead = False

    def checkDead(self):
        #Check if Ezzy's happiness is 0, if so, then the Ezzy is dead :(
        if self.happiness <= 0: self.dead = True

    def initiateStep(self):
        #Initiate step factor for the movement animation
        if self.ageIndex == 1: self.stepFactor = 20
        else: self.stepFactor = 10
        
    def initiateMoods(self, personality):
        #Initiates self.selectedMood that gives a list of pictures for the
        #different personality types (Rebel=0, Normal=1, Nerd=2)
        
        # Moods & Motions of normal Ezzy (that doesn't age)
        self.moods = [("ezzy.1.1.gif","ezzy.1.1.1.gif"), ("ezzy.1.2.gif","ezzy.1.2.1.gif"),
                      ("ezzy.1.3.gif", "ezzy.1.3.1.gif")]

        #Structure for self.moods(R/N):
        #   3-D List:
        #   Layer 1:
        #               [   Rebel or Nerd  ]
        #   Layer 2:
        #              [   [    young    ] , [    old    ]   ]
        #   Layer 3:
        #       [ [ (mood 1, mood 1 motion.1, mood 1 motion.2)] ,
        #         [ (mood 2, mood 2 motion.2, mood 2 motion.2)] ]

        self.moodsR = [ [("ezzy.rebel.young.1.gif","ezzy.rebel.young.1.1.gif"),
                        ("ezzy.rebel.young.2.gif","ezzy.rebel.young.2.1.gif")],
                       [("ezzy.rebel.old.1.gif","ezzy.rebel.old.1.1.gif",
                         "ezzy.rebel.old.1.2.gif"),
                        ("ezzy.rebel.old.2.gif","ezzy.rebel.old.2.1.gif",
                         "ezzy.rebel.old.2.2.gif")] ]
        self.moodsN = [ [("ezzy.nerd.young.1.gif","ezzy.nerd.young.1.1.gif"),
                        ("ezzy.nerd.young.2.gif","ezzy.nerd.young.2.1.gif")],
                       [("ezzy.nerd.old.1.gif","ezzy.nerd.old.1.1.gif",
                         "ezzy.nerd.old.1.2.gif"),
                        ("ezzy.nerd.old.2.gif","ezzy.nerd.old.2.1.gif",
                         "ezzy.nerd.old.2.2.gif")] ]
        
        #initiate list of moods that you will draw from
        if personality == 0: self.selectedMood = self.moodsR
        elif personality == 1: self.selectedMood = self.moods
        else: self.selectedMood = self.moodsN

    def moodSwing(self):
        # 1 out of 100 chance to turn on personality swing
        if self.Rebel == None and self.Nerd == None: return False
        elif self.Rebel == False:
            temp = random.randint(0,100)
            if temp == 0: 
                self.Rebel = True
                return True
        elif self.Nerd == False:
            temp = random.randint(0,100)
            if temp == 0: 
                self.Nerd = True
                return True

    def ageEzzy(self):
        #Over every 20 seconds, the age of Ezzy goes up by 1
        #From [0-49] Ezzy is young ; [50-100] Ezzy is old
        #Establishes self.ageIndex which refers to ___.old or ___.young
        if self.age != None:
            if self.counter == 20 and self.age < 100: self.age += 1
            if self.age < 50: self.ageIndex = 0
            elif self.age >= 50: self.ageIndex = 1

    def checkNeeds(self):
        #Decreases the moods of Ezzy over time
        if self.counter == 0 and self.energy > 0: self.energy -= 1
        elif self.counter == 5 and self.bladder > 0: self.bladder -= 1
        elif self.counter == 10 and self.fun > 0: self.fun -= 1
        elif self.counter == 15 and self.clean > 0: self.clean -= 1
        elif self.counter == 20 and self.hunger > 0: self.hunger -= 1
        self.happiness = self.bladder + self.fun + self.energy + self.clean + self.hunger
        
    def automaticCare(self):
        #As the needs of an Ezzy decreases, the more chances the Ezzy
        #will automatically on its own and care for itself
        checkList = [(self.bladder, 1),(self.energy, random.choice([0,2])),
         (self.fun, random.choice([3,4])), (self.clean, 5), (self.hunger, 7)]
        if self.doAutomatic == False:
            for check in checkList:
                if random.randint(0, int(check[0]**2)) == 0:
                    self.careIndex = check[1]
                    self.doAutomatic = True
                    break
                else: self.doAutomatic, self.careIndex = False, None
        
    def moveEzzy(self, new_x, new_y): #Move ezzy each time by a factor of:
        self.xfactor = (new_x - self.x)/self.stepFactor
        self.yfactor = (new_y - self.y)/self.stepFactor

    def changeMood(self): #Change the mood of Ezzies based on their needs
        if self.personality == 1: #Normal (has 3 moods)
            if ((self.happiness <= 25 and self.happiness > 0) or
                  (self.energy < 5 or self.bladder < 5 or self.fun < 5 or
                   self.clean < 5 or self.hunger < 5)):
                self.moodindex = 2
            elif ((self.happiness <= 50 and self.happiness > 25) or
                  (self.energy < 10 or self.bladder < 10 or self.fun < 10 or
                   self.clean < 10 or self.hunger < 10)):
                self.moodindex = 1
            elif self.happiness <= 75 and self.happiness > 50:
                self.moodindex = 0
        else: #Rebel or Nerd (has 2 moods)
            if ((self.happiness <= 25 and self.happiness > 0) or
                  (self.energy < 5 or self.bladder < 5 or self.fun < 5 or
                   self.clean < 5 or self.hunger < 5)):
                self.moodindex = 1
            else: self.moodindex = 0
    
    def drawEzzy(self, canvas): #Draw Ezzy on the canvas
        winWidth, winHeight = 1000, 490
        if self.x < 0: self.x = 0
        elif self.x > winWidth: self.x = winWidth
        if self.y < 0: self.y = 0
        elif self.y > winHeight: self.y = winHeight
        if self.drawOn == True and self.dead == False:
            if self.personality == 1:
                self.image = PhotoImage(file="%s" %
                    (self.selectedMood[self.moodindex][self.motion]))
                canvas.create_image(self.x, self.y, image = self.image)
            else:
                self.image = PhotoImage(file="%s" %
                    (self.selectedMood[self.ageIndex][self.moodindex][self.motion]))
                canvas.create_image(self.x, self.y, image = self.image)
        elif self.dead == True:
            self.image = PhotoImage(file="ezzy.dead.gif")
            canvas.create_image(self.x, self.y, image=self.image)
        

##########

game = runGame()
game.run()
