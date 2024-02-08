import pygame
import math
import os
from game import currentTurn,setCurScene
promotedPawns = {}
takenPieces = []
images = []
loadImg = {}
for root, dirs, files in os.walk("images"):
    for file in files:
        images.append(file)
for image in images:
    loadImg.update({image[0:-4]: pygame.image.load("images\\" + image)})
screenWidth = 800
screenHeight = 800
pieceStats = {}
Grid = {}
screen = pygame.display.set_mode(size=(screenWidth, screenHeight))
clock = pygame.time.Clock()
selector = None
running = True

def initGrid ():
    pieceList = initPieces()
    for color in ["W", "B"]:
        pawnYGrid = 2
        royalYGrid = 1
        if color == "B":
            pawnYGrid = 7
            royalYGrid = 8
        for num in range(1, 9):
            Grid.update({(num, pawnYGrid) : pieceList[num - 1] + color})
            pieceStats.update({pieceList[num - 1] + color : {"moved" : False, 'promotion' : False}})
            if pieceList[num + 7][1] == "k":
                Grid.update({(num, royalYGrid) : pieceList[num + 7] + color})
                pieceStats.update({pieceList[num + 7] + color : {"moved" : False}})
            else:
                Grid.update({(num, royalYGrid) : pieceList[num + 7] + color})
                pieceStats.update({pieceList[num + 7] + color : {"moved" : False}})
              
def initPictures ():
    ChessBoard = pygame.image.load("Chessboard.png")
    screen.blit(ChessBoard, (0, 0))

    keyList = list(Grid.keys())
    valList = list(Grid.values())
    for piece in pieceStats:
        if piece not in valList:
            if piece not in takenPieces:
                takenPieces.append(piece)
                pieceStats[piece]['moved'] = True 
        else:
            position =  valList.index(piece)
            pieceStats[piece].update({"location" : calculateCoordinatesFromGrid(keyList[position])})
            if piece in promotedPawns:
                screen.blit(loadImg[promotedPawns[piece] + piece[-1]], pieceStats[piece]["location"])
            else:
                screen.blit(loadImg[piece[1:3]], pieceStats[piece]["location"])
    pygame.display.update()

def initPieces():
    pieces = []
    for x in range(1,9):
        pieces.append( str(x) + "p")
    pieces.extend(["1r", "1h", "1b", "1q", "1k", "2b", "2h", "2r"])
    return pieces


def calculatePositionByClick(pos):
    xPos = pos[0]
    xPos = math.ceil(xPos / (screenWidth/8))
    yPos = abs((pos[1] - screenHeight)) / (screenWidth/8)
    yPos = math.ceil(yPos)
    return (xPos, yPos)

def calculateCoordinatesFromGrid(pos):
    return (pos[0] *(screenWidth/8) - (screenWidth/8) , abs(pos[1] *(screenWidth/8)  - screenHeight))

def initPromotion():
    promotionSquare = pygame.image.load('promotion.png')
    queenSq = pygame.image.load("images\\" + "q" + currentTurn() + '.png')
    RookSq = pygame.image.load("images\\" + "r" + currentTurn() + '.png')
    bishopSq = pygame.image.load("images\\" + "b" + currentTurn() + '.png')
    horseSq = pygame.image.load("images\\" + "h" + currentTurn() + '.png')
    screen.blit(promotionSquare, (200, 400))
    screen.blit(promotionSquare, (300, 400))
    screen.blit(promotionSquare, (400, 400))
    screen.blit(promotionSquare, (500, 400))
    screen.blit(queenSq, (200, 400))
    screen.blit(RookSq, (300, 400))
    screen.blit(bishopSq, (400, 400))
    screen.blit(horseSq, (500, 400))

    