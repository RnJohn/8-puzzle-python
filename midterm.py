import cv2 
from skimage import io
import numpy as np
np.set_printoptions(threshold=np.inf)

class Piece: 
    def __init__(self,image, i, j, blank): #Constructor
        self.portion = [[]]
        self.isBlank = False
        if not blank:
            for x in range(i,i+100):
                temp = []
                for y in range(j,j+100):
                    temp.append(image[x][y])
                self.portion.append(temp)
        else:
            for x in range(100):
                temp = []
                for y in range(100):
                    temp.append([0,0,0])
                self.portion.append(temp)
            self.isBlank = True
        self.portion.pop(0)

class Puzzle:
    def __init__(self): #Constructor
        self.positions = [[]]
        self.positions.pop(0)
        self.f = 0

    def add(self,pieces): #Add a row of pieces to the positions matrix
        self.positions.append(pieces)

    def calculatef(self,goal): #Calculate the f value, comparing each position of this puzzle to the goal puzzle
        for x in range(3):
            for y in range(3):
                if self.positions[x][y] != goal.positions[x][y]:
                    self.f = self.f + 1

    def findBlank(self): #Find the coordinates of the blank space
        for x in range(3):
            for y in range(3):
                if (self.positions[x][y].isBlank == True):
                    return x,y

    def getChildren(self): #Generate all the alternatives of moving the blank space
        x,y = currentPuzzle.findBlank()
        children = []
        if (self.checkPossibleMove(x,y+1)):
            temp = Puzzle()
            temp.positions = self.exchange(x,y+1,x,y) 
            children.append(temp)
        if (self.checkPossibleMove(x,y-1)):
            temp = Puzzle()
            temp.positions = self.exchange(x,y-1,x,y) 
            children.append(temp)
        if (self.checkPossibleMove(x+1,y)):
            temp = Puzzle()
            temp.positions = self.exchange(x+1,y,x,y)
            children.append(temp)
        if (self.checkPossibleMove(x-1,y)):
            temp = Puzzle()
            temp.positions = self.exchange(x-1,y,x,y)
            children.append(temp)
        return children
        
    def exchange(self,x1,y1,x2,y2): #Move the blank space
        tempPositions = self.positions
        temp = tempPositions[x1][y1]
        tempPositions[x1][y1] = tempPositions[x2][y2]
        tempPositions[x2][y2] = temp
        return tempPositions
        
    def checkPossibleMove(self,x,y): #Check if moving the blank space won't be out of bounds
        if x >= 0 and x < len(self.positions) and y >= 0 and y < len(self.positions):
            return True
        else:
            return False


image = io.imread('https://res.cloudinary.com/demo/image/upload/h_300,w_300,c_pad,b_auto:predominant_gradient:4:palette_red_green_blue_orange/horse.jpg')

piece1 = Piece(image,0,0,False)
piece2 = Piece(image,0,100,False)
piece3 = Piece(image,0,200,False)
piece4 = Piece(image,100,0,False)
piece5 = Piece(image,100,100,False)
piece6 = Piece(image,100,200,False)
piece7 = Piece(image,200,0,False)
piece8 = Piece(image,200,100,False)
piece9 = Piece(image,0,0,True)

goal = Puzzle()
goal.add([piece1,piece2,piece3])
goal.add([piece4,piece5,piece6])
goal.add([piece7,piece8,piece9])

start = Puzzle()
start.add([piece1,piece2,piece3])
start.add([piece9,piece4,piece6])
start.add([piece7,piece5,piece8])

openList = []
closedList = []
openList.append(start)

print(openList[0] == start)

# while True:
#     currentPuzzle = openList[0]
#     currentPuzzle.calculatef(goal)
#     print(currentPuzzle.positions)
#     if (currentPuzzle.f == 0):
#         print("Found")
#         break
#     children = currentPuzzle.getChildren()
#     for x in children:
#         x.calculatef(goal)
#         openList.append(x)
#     openList.pop(0)
#     openList.sort(key = lambda x:x.f,reverse=False)