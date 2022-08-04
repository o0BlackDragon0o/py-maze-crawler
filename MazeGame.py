#code written by Sam Baverstock
import turtle
import tkinter as tk
from copy import deepcopy # allows the copying of 2D lists
import time
import random

##starting variables
pPos = [1, 1] #position of the player inside the labyrinth
pDir = 0 #player direction, 0 is up/north, 1 left/west, 2 down/south, and 3 right/east (numbers count up in 90 degree anticlockwise increments)
hudIsShown = False

##mazes
#array collumns must all be equal, as with rows eg. 10x10 8x5 ect.
# the @ character denotes a wall, and the . denotes emplty space S denotes the players start pos, F is the exit
# the generateMaze() function will create these at the given size
#examples:

exampleMaze =  [['@', '@', '@', '@', '@'],
                ['@', 'S', '@', '.', 'F'],
                ['@', '.', '@', '.', '@'],
                ['@', '.', '.', '.', '@'],
                ['@', '@', '@', '@', '@']]

testMaze = [['@', '@', '@', '@', '@', '@', '@'],
            ['@', '.', '@', '.', '@', '@', '@'],
            ['@', 'S', '@', '.', '.', '.', '@'],
            ['@', '.', '.', '.', '@', '.', '@'],
            ['@', '@', '.', '@', '@', '.', '@'],
            ['@', '@', '@', '@', '@', 'F', '@']]

newMaze = [] #maze used for random mazes
#make sure that currentMaze is set
sizeMaze = [5, 5]
currentMaze = testMaze

## sprites are lists of coordinates that get drawn to the screen connect the dots style
#Hud sprites
triangle_sprite = [[0, 50], [-35, -50], [35, -50], [0, 50]]
wallHudIcon = [[-10, 10], [10, 10], [10, -10], [-10, -10], [-10, 10], [10, -10], [-10, -10], [10, 10]]
playerIcon = [[0, 8], [-5, -8], [5, -8], [0, 8]]
finishIcon = [[-4, -8], [-4, 8], [8, 4], [-4, 0]]
testSprite = [[-10,-10], [10, 10], [10, -5]]
#Wall sprites
front0 = [[550, 330], [400, 240], [400, -240], [-400, -240], [-400, 240], [400, 240], [-400, 240], [-550, 330]]
front0Right = [[550, 240], [400, 240], [400, -240], [550, -240]]
side0 = [[550, 330], [400, 240], [400, -240], [550, -330]]

front1 = [[400, 240], [250, 150], [250, -150], [-250, -150], [-250, 150], [250, 150], [-250, 150], [-400, 240]]
front1Right = [[400, 150], [250, 150], [250, -150], [400, -150]]
side1 = [[250, 150], [550, 330], [400, 240], [400, -240], [250, -150], [250, 150]]

front2 = [[250, 150], [150, 90], [150, -90], [-150, -90], [-150, 90], [150, 90], [-150, 90], [-250, 150]]
front2Right = [[250, 90], [150, 90], [150, -90], [250, -90]]
side2 = [[150, 90], [400, 240], [250, 150], [250, -150], [150, -90], [150, 90]]

front3 = [[150, 90], [100, 60], [100, -60], [-100, -60], [-100, 60], [100, 60], [-100, 60], [-150, 90]]
front3Right = [[150, 60], [100, 60], [100, -60], [150, -60]]
side3 = [[100,60], [250, 150], [150, 90], [150, -90], [100, -60], [100, 60]]

#makes it seem as if there is more maze ahead
front4 = [[-80, -50], [-100, -60], [-100, 60], [-80, 50], [-100, 60], [100, 60], [80, 50], [100, 60], [100, -60], [80, -50]]

def createPen(penName, penColor): # creates a pen to use. use as penName = createPen(*args)
    penName = turtle.Turtle()
    penName._delay(0)
    penName.speed(0)
    penName.shape("square")
    penName.color(penColor)
    return penName

def initiateGraphics(): ## creates a pen for system puposes called systemPen, then draws a bounding box for screen, and adds the instructions
    createWindow(1200,760,"Maze Exploration Game")
    global systemPen
    systemPen = createPen("systemPen", "white")
    systemPen.penup()
    systemPen.hideturtle()
    systemPen.goto(-screenWidth/2 + 50, -screenHeight/2 +50)
    systemPen.pendown()
    systemPen.setheading(0)
    
    for i in range(2): #draw bounding box based on window size
        systemPen.forward(screenWidth-100)
        systemPen.left(90)
        systemPen.forward(screenHeight-100)
        systemPen.left(90)
    systemPen.penup()
    systemPen.goto(0, 330)
    systemPen.write("Arrow Keys/WASD = Move                 M = Toggle Map", font=("arial", 30, 'normal'), align = 'center')
    systemPen.goto(-10,-370)
    systemPen.write("Objective: get to the flag!", font=("arial", 20, 'normal'), align = 'center')


def createWindow(xSize,ySize,windowName): #creates a winow of x,y size, default name for window is wn
    global wn
    wn = turtle.Screen()
    wn.title(windowName)
    wn.bgcolor("black")
    global screenWidth
    global screenHeight
    screenWidth = xSize
    screenHeight = ySize
    wn.setup(width=screenWidth, height=screenHeight)
    wn.tracer(0)

def vector(xStart,yStart,xEnd,yEnd,pen, oReturn = None): #draws a line between two points
    pen.penup()
    pen.goto(xStart,yStart)
    pen.pendown()
    pen.goto(xEnd,yEnd)
    pen.penup()
    if (oReturn == True):
        pen.goto(0,0)

def drawSprite(spriteCoords, xOffset, yOffset, pen, scale = 1, mirror = None, rotation = None, color = 'white'): #create a sprite connect the dots style from an array of given coordinates
    spriteCoordRef = deepcopy(spriteCoords)
    penColor = pen.color
    if scale != 1 or scale != None: #scale the sprite by the given magnification eg. 2 = twice as big
        for i in range(len(spriteCoordRef)):
            spriteCoordRef[i][0] = spriteCoordRef[i][0] * scale
            spriteCoordRef[i][1] = spriteCoordRef[i][1] * scale
    
    if mirror == True:#mirror sprite along the y axis (flip horizontally)
        
        for i in range(len(spriteCoordRef)):
            spriteCoordRef[i][0] = - spriteCoordRef[i][0]            
    
    if rotation != None: #rotate the sprite in increments of 90 degrees
        for i in range(len(spriteCoordRef)):
            x, y = spriteCoordRef[i]
            if rotation == 1:
                spriteCoordRef[i] = [-y, x]
            elif rotation == 2:
                spriteCoordRef[i] = [-x, -y]
            elif rotation == 3:
                spriteCoordRef[i] = [y, -x]
            else: 
                if rotation != 0: print("rotation of sprite {spriteCoords} is outside range 0-3")             
    rotation = None

    pen.color(color)

    for i in range(len(spriteCoordRef) - 1): #draw the sprite
        if len(spriteCoordRef) > i:
            xStart, yStart = spriteCoordRef[i]
            xEnd, yEnd = spriteCoordRef[i+1]
            xStart, yStart, xEnd, yEnd = xStart + xOffset, yStart + yOffset, xEnd + xOffset, yEnd + yOffset # include offset
            vector(xStart, yStart, xEnd, yEnd, pen)

    pen.color = penColor


def generateMaze(xSize, ySize, printMaze = False): #generates mazes based on the depth first search algorithm (all code is still original)
    name = [] #temp variable that holds the maze array
    
    if xSize %2 == 0: #make sure x and y are odd and more than 4
        xSize = xSize - 1
        if xSize < 5: xSize = 5
    if ySize %2 == 0:
        ySize = ySize - 1
        if ySize < 5: ySize = 5

    for i in range(ySize): #create a 2D list of the correct size containing only walls
        newRow = []
        for i in range(xSize):
            newRow.append('@')
        name.append(newRow)

    ##generate maze from the made array
    #uses a custom implementation of the random depth first search algorith
    global visitedCells
    visitedCells = []
    cellQueue = []

    #pick and set starting cell from any odd cell (1,1)(5,7) etc. even cells are used to connect odd ones together
    startingCell = [random.randrange(1, ySize, 2), random.randrange(1, xSize, 2)]
    cellQueue.insert(0, startingCell) #push the cell to the queue, and add to visited cells
    visitedCells.append(startingCell)
    name[startingCell[0]][startingCell[1]] = 'S' #set the start on the grid, and set pPos to the start
    global pPos
    pPos = [startingCell[1], startingCell[0]]

    finishCell = [[1, 1], 0] #[coord of finish, distance to the start]
    while cellQueue != []: #until the cell queue is empty
        startStrand(cellQueue, name) #create a new maze strand at the curent cell
        if len(cellQueue) >= finishCell[1]: #set a new finish if curernt cell is further away
            finishCell = [[cellQueue[0][0], cellQueue[0][1]], len(cellQueue)]
        cellQueue.pop(0) #once reaching a dead end, remove the current cell from the queue, try again from one cell back
    #once the cell queue is empty and the while loop exits, the grid should be filled with a maze.
        
    #set finish cell in the grid
    name[finishCell[0][0]][finishCell[0][1]] = 'F'

    if printMaze == True:
        for i in name:
             print(name)
    return name

def startStrand(cellQueue, name): #creates a new maze strand from the current cell
    i = 0
    if cellSelection(cellQueue[0], name, visitedCells) == False: #exit if no strands can be created from the current cell
        return False
    while cellSelection(cellQueue[0], name, visitedCells) != False and i < 100: #while the strand can continue (upper limit of 100 to prevent possible infinite loops)
        i = i + 1
        newCell = cellSelection(cellQueue[0], name, visitedCells) #randomly pick an adjacent cell
        name[newCell[0]][newCell[1]] = '.' #set that cell to empty

        #work out the corridor between the new and last cell, set it to empty
        cellWall = [int(cellQueue[0][0]) + int((newCell[0] - cellQueue[0][0])/2), int(cellQueue[0][1]) + int((newCell[1] - cellQueue[0][1])/2)]
        name[cellWall[0]][cellWall[1]] = '.'
        cellQueue.insert(0, newCell)#push the new cell to the queue
        visitedCells.append(newCell)#add it to the list of visited cells
    return True


def cellSelection(cell, maze, visitedCells): #picks a random unvisited ajecent cell, or returns false if no cells are valid
    #variables store the adjecent cells
    upCell = [int(cell[0] - 2), int(cell[1])]
    leftCell = [int(cell[0]), int(cell[1] - 2)]
    downCell = [int(cell[0] + 2), int(cell[1])]
    rightCell = [int(cell[0]), int(cell[1] + 2)]
    adjCells = [upCell, leftCell, downCell, rightCell] #list of all adjecent cells
    
    availCells = [] #list to hold the valid cells
    
    for i in range(len(adjCells)): #check if each adjacent cell is valid to pick from (is unvisited and inside the maze)
        if doesElementExistInList(adjCells[i], visitedCells) == False:
            if adjCells[i][0] > 0 and adjCells[i][0] < len(maze) and adjCells[i][1] > 0 and adjCells[i][1] < len(maze[0]):            
                availCells.append(adjCells[i])
    # print("Visited Cells: {}".format(visitedCells))
    # print("availCells: {}".format(availCells))
    
    if availCells != []:
        return random.choice(availCells) #return the picked cell

    else: return False #if no cells were valid, return False

def doesElementExistInList(element, listToCheck): #function that checks if a given variable exists within a list, used to check if a cell has been visited
    for i in range(len(listToCheck)):
        if listToCheck[i] == element:
            # print("List element {} found in list".format(element))
            return True            
    return False  

def drawMapHud(mapArray): #draw the map hud on the screen
    currentRow = 0
    hudX , hudY = -screenWidth/2 + 100, screenHeight/2 - 70 #Top left corner of hud coords
    for i in range(len(mapArray)): #cycle through each row
        for i in range(len(mapArray[0])): #cycle each element currently in the row
            if mapArray[currentRow][i] == "@": #check if a wall exists at the current square
                drawSprite(wallHudIcon, (hudX + i * 20) + 20 , (hudY + (-currentRow - 1) * 20) , hudPen, 1, False, 0)
            elif mapArray[currentRow][i] == "F":#check if the finish exists at the current cell
                drawSprite(finishIcon, (hudX + i * 20) + 20 , (hudY + (-currentRow - 1) * 20), hudPen, 1, None, None, "red")

        currentRow = currentRow + 1    

    #draw a box around the hud
    hudWidth = 20 + (len(mapArray[0]) * 20)
    hudHeight = 20 + (len(mapArray) * 20)
    vector(hudX, hudY, hudX + hudWidth, hudY, hudPen) #top
    vector(hudX + hudWidth, hudY, hudX + hudWidth, hudY - hudHeight, hudPen) #right
    vector(hudX + hudWidth, hudY - hudHeight, hudX, hudY - hudHeight, hudPen) #bottom
    vector(hudX, hudY - hudHeight,hudX, hudY, hudPen) #left
    
def updateHud():#updates the map hud and player position on the screen
    x, y =  -screenWidth/2 + 100, screenHeight/2 - 70
    
    if hudIsShown == True:
        hudPen.clear()
        drawMapHud(currentMaze)
        drawSprite(playerIcon, (x + pPos[0] * 20) + 20 , (y + (-pPos[1] - 1) * 20), hudPen, 1, False, pDir, "yellow")   

def updateFrame(): #draws the maze on screen based on where you are in the maze array and what direction you are facing
    #Right Side0
    if posWallCheck(0, 1) == True:
        drawSprite(side0, 0, 0, framePen)
    elif posWallCheck(1, 1) == True:
        drawSprite(front0Right, 0, 0, framePen)
    
        #Left Side0
    if posWallCheck(0, -1) == True:
        drawSprite(side0, 0, 0, framePen, 1, True)
    elif posWallCheck(1, -1) == True:
        drawSprite(front0Right, 0, 0, framePen, 1, True)

    
    #1-3 row sides
    if posWallCheck(1, 0) == False:
        if posWallCheck(1, 1) == True:
            drawSprite(side1, 0, 0, framePen)
        elif posWallCheck(2, 1) == True:
            drawSprite(front1Right, 0, 0, framePen)
        if posWallCheck(1, -1) == True:
            drawSprite(side1, 0, 0, framePen, 1, True)
        elif posWallCheck(2, -1) == True:
            drawSprite(front1Right, 0, 0, framePen, 1, True)
        #2nd row sides
        if posWallCheck(2, 0) == False:
            if posWallCheck(2, 1) == True:
                drawSprite(side2, 0, 0, framePen)
            elif posWallCheck(3, 1) == True:
                drawSprite(front2Right, 0, 0, framePen)
            if posWallCheck(2, -1) == True:
                drawSprite(side2, 0, 0, framePen, 1, True)
            elif posWallCheck(3, -1) == True:
                drawSprite(front2Right, 0, 0, framePen, 1, True)
            #3rd row sides
            if posWallCheck(3, 0) == False:
                if posWallCheck(3, 1) == True:
                    drawSprite(side3, 0, 0, framePen)
                elif posWallCheck(4, 1) == True:
                    drawSprite(front3Right, 0, 0, framePen)
                if posWallCheck(3, -1) == True:
                    drawSprite(side3, 0, 0, framePen, 1, True)
                elif posWallCheck(4, -1) == True:
                    drawSprite(front3Right, 0, 0, framePen, 1, True)
        
    #front Walls
    if posWallCheck(1, 0) == True:

        drawSprite(front0, 0, 0, framePen)
    elif posWallCheck(2, 0) == True:

        drawSprite(front1, 0, 0, framePen)
    elif posWallCheck(3, 0) == True:

        drawSprite(front2, 0, 0, framePen)
    elif posWallCheck(4, 0) == True:

        drawSprite(front3, 0, 0, framePen)
    else:
        drawSprite(front4, 0, 0, framePen)
    
def setCurrentMaze(mazeArray): #changes the current maze
    global currentMaze
    currentMaze = deepcopy(mazeArray)    
    
def posWallCheck(fdOffset, sideOffset): #checks a position in the maze  for a wall in relation to the player. for side offsets positive values check to the right of the player, negative to the left
    global pPos
    global pDir
    global currentMaze
    posToCheck = [0, 0]

    try:
        if pDir % 2 == 0: #up or down             
            posToCheck[0] = int(pPos[0] + (sideOffset * -(pDir - 1)))
            posToCheck[1] = int(pPos[1] + (fdOffset * (pDir - 1)))
           
        else: #left - or right +
            posToCheck[0] = int(pPos[0] + (fdOffset * (pDir - 2)))
            posToCheck[1] = int(pPos[1] + (sideOffset * (pDir - 2)))
            
        if currentMaze[posToCheck[1]][posToCheck[0]] == '@':
            #print('Wall')
            return True

        # if currentMaze[posToCheck[1]][posToCheck[0]] == 'F':
        #     return 'finish'
        return False

    except Exception as raisedExeption: #the position is outside of the maze
        print(raisedExeption)
        return False
 
def left():
    if hudIsShown == False:
        global pDir
        pDir = pDir + 1
        if pDir > 3:
            pDir = 0
        update()

def right():
    if hudIsShown == False:
        global pDir
        pDir = pDir - 1
        if pDir < 0:
            pDir = 3
        update()

def forward():
    if hudIsShown == False:
        global pDir
        global pPos
        global currentMaze
        if pDir % 2 == 0: #up or down
            newPos = pPos[1] + (pDir - 1)
            if currentMaze[newPos][pPos[0]] != '@':
                if currentMaze[newPos][pPos[0]] == 'F':
                    finishMaze()
                    return           
                pPos[1] = newPos
                
        else: #left or right
            newPos = pPos[0] + (pDir - 2)
            if currentMaze[pPos[1]][newPos] != '@':
                if currentMaze[pPos[1]][newPos] == 'F':
                    finishMaze()
                    return            
                pPos[0] = newPos
        update()

def back():
    if hudIsShown == False:
        global pDir
        global pPos
        global currentMaze
        if pDir % 2 == 0: #up or down
            newPos = pPos[1] - (pDir - 1)
            if currentMaze[newPos][pPos[0]] != '@':
                if currentMaze[newPos][pPos[0]] == 'F':
                    finishMaze()
                    return           
                pPos[1] = newPos
                
        else: #left or right
            newPos = pPos[0] - (pDir - 2)
            if currentMaze[pPos[1]][newPos] != '@':
                if currentMaze[pPos[1]][newPos] == 'F':
                    finishMaze()
                    return            
                pPos[0] = newPos
        update()

def toggleHud():
    global hudIsShown
    if hudIsShown == True:
        hudIsShown = False
        hudPen.clear()
        update()
    else:
        hudIsShown = True
        framePen.clear()
        drawMapHud(currentMaze)
        updateHud()

def newMaze(xSize = 0, ySize = 0):
    if xSize == 0:
        xSize = random.randrange(5, 51, 2)
        ySize = random.randrange(5, 31, 2)

    newMaze = generateMaze(xSize, ySize)
    setCurrentMaze(newMaze)
    update()
    if hudIsShown == True:
        framePen.clear()


def finishMaze():
    print("maze completed")
    framePen.clear()
    hudPen.clear()
    framePen.goto(0, 0)
    framePen.write("Congratulations you have escaped\n Press P to generate a new Maze\n             Press space to exit", font=("arial", 48, 'normal'), align = 'center')
    turtle.listen()
    turtle.onkey(exitProg, 'space')

def smallBttnClk():
    global sizeMaze
    sizeMaze = [11, 11]
    mWindow.destroy()

def medBttnClk():
    global sizeMaze
    sizeMaze = [17, 17]
    mWindow.destroy()

def largeBttnClk():
    global sizeMaze
    sizeMaze = [29, 29]
    mWindow.destroy()

def menuWindow():
    global mWindow
    mWindow = tk.Tk()
    mWindow.title("Maze Game Menu")
    mWindow.geometry("500x300")
    mWindow.eval("tk::PlaceWindow . center")
    menuLabel = tk.Label(mWindow,text="Welcome to the maze exploration game\nPlease select a maze size", font=("Arial",20), justify="center")
    menuLabel.pack()

    smallBttn = tk.Button(mWindow, text="Small - 11 x 11", command=smallBttnClk, font=("Arial",20), width=15, bg='#c4c4c4')
    smallBttn.pack()
    medBttn = tk.Button(mWindow, text="Medium - 17 x 17", command=medBttnClk, font=("Arial",20), width=15, bg='#c4c4c4')
    medBttn.pack()
    largeBttn = tk.Button(mWindow, text="Large 29 x 29", command=largeBttnClk, font=("Arial",20), width=15, bg='#c4c4c4')
    largeBttn.pack()

    mWindow.mainloop()


def onStart():    ## Runs before the update loop   
    initiateGraphics()
    global hudPen
    hudPen = createPen("hudPen", "White")
    global framePen
    framePen = createPen("framePen", "white")
    drawSprite(finishIcon, 150, -353, systemPen, 1.5, None, None, "red")
    newMaze(sizeMaze[0], sizeMaze[1])
    update()
    
def callUpdate(): #if you are not using a event based grafics interface like turtle, this can be called under on start to run the update at a semi fixed period. delta time is given for consistency between updates.
    prevTime = time.time() # sets prev time when update has not been called before
    global deltaTime
    while True:
        currentTime = time.time() #just contains the current time, used to calculate deltaTime
        deltaTime = currentTime - prevTime #this is the change (delta) in time between this update and last update. it allows for consistant variable changes even with variances in update calls

        update()

        prevTime = currentTime
        time.sleep(0.05) #prevents the update from being called too frequently

def update(): # this is where anything that happens whilst the game is running is called, make sure to call it on onkey() if using turtle
    framePen.clear()
    if hudIsShown == True:
        updateHud()
    updateFrame()

def exitProg(): #exits the program.
    wn.bye()
    quit()

def main():
    menuWindow()
    onStart()
    turtle.listen()
    turtle.onkey(left, 'a')
    turtle.onkey(left, "Left")
    turtle.onkey(right, "d")
    turtle.onkey(right, "Right")
    turtle.onkey(forward, "w")
    turtle.onkey(forward, "Up")
    turtle.onkey(back, "s")
    turtle.onkey(back, "Down")
    turtle.onkey(newMaze, "p")
    turtle.onkey(toggleHud, "m")
    
   
if __name__ == "__main__":
    main()
    
    turtle.mainloop()


    
