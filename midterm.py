import cv2 
from skimage import io
import numpy as np
np.set_printoptions(threshold=np.inf)

class Piece:
    def __init__(self,index,image, i, j, blank): #Constructor
        self.index = index
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
    def __init__(self, g): #Constructor
        self.positions = [[]]
        self.positions.pop(0)
        self.f = 0
        self.h = 0
        self.g = g

    def add(self,pieces): #Add a row of pieces to the positions matrix
        self.positions.append(pieces)

    def calculateh(self,goal): #Calculate the f value, comparing each position of this self to the goal self
        h = 0
        for x in range(3):
            for y in range(3):
                if self.positions[x][y] != goal.positions[x][y] and self.positions[x][y].isBlank == False:
                    h = h + 1
        return h

    def calculatef(self,goal):
        return self.h+self.g

    def findBlank(self): #Find the coordinates of the blank space
        for x in range(3):
            for y in range(3):
                if (self.positions[x][y].isBlank == True):
                    return x,y

    def getChildren(self): #Generate all the alternatives of moving the blank space
        x,y = currentPuzzle.findBlank()
        children = []
        if (self.checkPossibleMove(x,y+1)):
            temp = Puzzle(self.g+1)
            temp.positions = self.exchange(x,y+1,x,y) 
            children.append(temp)
        if (self.checkPossibleMove(x,y-1)):
            temp = Puzzle(self.g+1)
            temp.positions = self.exchange(x,y-1,x,y) 
            children.append(temp)
        if (self.checkPossibleMove(x+1,y)):
            temp = Puzzle(self.g+1)
            temp.positions = self.exchange(x+1,y,x,y)
            children.append(temp)
        if (self.checkPossibleMove(x-1,y)):
            temp = Puzzle(self.g+1)
            temp.positions = self.exchange(x-1,y,x,y)
            children.append(temp)
        return children
        
    def exchange(self,x1,y1,x2,y2): #Move the blank space
        tempPositions = self.copy(self.positions)
        temp = tempPositions[x1][y1]
        tempPositions[x1][y1] = tempPositions[x2][y2]
        tempPositions[x2][y2] = temp
        return tempPositions

    def copy(self,positions):
        temp = []
        for x in range(3):
            temp.append(positions[x])
        return temp

        
    def checkPossibleMove(self,x,y): #Check if moving the blank space won't be out of bounds
        if x >= 0 and x < 3 and y >= 0 and y < 3:
            return True
        else:
            return False

    def displayImage(self):
        p1 = self.positions[0][0].portion
        p2 = self.positions[0][1].portion
        p3 = self.positions[0][2].portion
        p4 = self.positions[1][0].portion
        p5 = self.positions[1][1].portion
        p6 = self.positions[1][2].portion
        p7 = self.positions[2][0].portion
        p8 = self.positions[2][1].portion
        p9 = self.positions[2][2].portion

        row1 = self.constructRow(p1,p2,p3)
        row2 = self.constructRow(p4,p5,p6)
        row3 = self.constructRow(p7,p8,p9)

        temp = np.asarray(self.constructImage(row1,row2,row3))

        #print(temp.shape)
        io.imshow(temp)
        io.show()


    def constructRow(self, piece1, piece2, piece3):
        resultMatrix = [[]]
        resultMatrix.pop(0)
        for x in range(100):
            tempVector = []
            for y in range(100):
                tempVector.append(piece1[x][y])
            for y in range(100):
                tempVector.append(piece2[x][y])
            for y in range(100):
                tempVector.append(piece3[x][y])
            resultMatrix.append(tempVector)
        return resultMatrix


    def constructImage(self, row1, row2, row3):
        resultMatrix = [[]]
        resultMatrix.pop(0)
        for y in range(100):
            resultMatrix.append(row1[y])
        for y in range(100):
            resultMatrix.append(row2[y])
        for y in range(100):
            resultMatrix.append(row3[y])
        return resultMatrix

    def displayPieces(self):
        print("------------")
        print("| ",self.positions[0][0].index,"|",self.positions[0][1].index,"|",self.positions[0][2].index,"|")
        print("------------")
        print("| ",self.positions[1][0].index,"|",self.positions[1][1].index,"|",self.positions[1][2].index,"|")
        print("------------")
        print("| ",self.positions[2][0].index,"|",self.positions[2][1].index,"|",self.positions[2][2].index,"|")





image = io.imread('https://res.cloudinary.com/demo/image/upload/h_300,w_300,c_pad,b_auto:predominant_gradient:4:palette_red_green_blue_orange/horse.jpg')

piece1 = Piece(1,image,0,0,False)
piece2 = Piece(2,image,0,100,False)
piece3 = Piece(3,image,0,200,False)
piece4 = Piece(4,image,100,0,False)
piece5 = Piece(5,image,100,100,False)
piece6 = Piece(6,image,100,200,False)
piece7 = Piece(7,image,200,0,False)
piece8 = Piece(8,image,200,100,False)
piece9 = Piece(9,image,0,0,True)

goal = Puzzle(0)
goal.add([piece1,piece2,piece3])
goal.add([piece4,piece5,piece6])
goal.add([piece7,piece8,piece9])

start = Puzzle(0)
start.add([piece2,piece1,piece3])
start.add([piece7,piece6,piece9])
start.add([piece5,piece8,piece4])

start.f = start.calculatef(goal)
start.h = start.calculateh(goal)
openList = []
openList.append(start)

#print(openList[0] == start)
#print(type(image))
#print(type(piece1.portion))
#goal.displayImage()

while True:
    currentPuzzle = openList[0]
    #print(currentPuzzle.positions)
    #currentPuzzle.displayImage() 
    #print("monda")
    #currentPuzzle.displayPieces()
    print(currentPuzzle.h)
    if (currentPuzzle.h == 0):
        print("Found")
        break
    children = currentPuzzle.getChildren()
    for x in children:
        x.f = x.calculatef(goal)
        x.h = x.calculateh(goal)
        openList.append(x)
    del openList[0]
    openList.sort(key = lambda x:x.f, reverse=False)