import pygame
from chessPiecesInnit import calculateCoordinatesFromGrid, calculatePositionByClick, Grid, pieceStats, initGrid, screen, initPromotion, initPictures, promotedPawns
from game import currentTurn, changeSceneToPromotion, getCurScene, setCurScene, itterateTurn, getTurn
import copy
allPossibleMoves = {}

previousPiece = ''
previousMove = ''
lastPawn = []
def posHorseSquares(curPosition, color, board=Grid):
    possibleMovement = []
    onesArray = [-1, 1]
    twosArray = [-2, 2]
    bothArray = onesArray + twosArray
    xPos = curPosition[0]
    yPos = curPosition[1]
    for nums in bothArray:
        if abs(nums) == 1:
            for twos in twosArray:
                if not ((xPos + nums > 8 or xPos + nums < 1) or (yPos + twos > 8 or yPos + twos < 1)):
                    if not (xPos + nums, yPos + twos) in board:
                        possibleMovement.append((xPos + nums, yPos + twos))
                    elif board[(xPos + nums, yPos + twos)][-1] != color:
                        possibleMovement.append((xPos + nums, yPos + twos))
                    
        if abs(nums) == 2:
            for ones in onesArray:
                if not ((xPos + nums > 8 or xPos + nums < 1) or (yPos + ones > 8 or yPos + ones < 1)):
                    if not (xPos + nums, yPos + ones) in board:
                        possibleMovement.append((xPos + nums, yPos + ones))
                    elif board[(xPos + nums, yPos + ones)][-1] != color:
                        possibleMovement.append((xPos + nums, yPos + ones))

    return possibleMovement

def posPawnSquares(curPosition, color, board=Grid):
    global promotedPawns
    if board[curPosition] in promotedPawns:
        if promotedPawns[board[curPosition]] == 'q':
            return posQueenSquares(curPosition, color, board)
    if board[curPosition] in promotedPawns:
        if promotedPawns[board[curPosition]] == 'r':
            return posRookSquares(curPosition, color, board)
    if board[curPosition] in promotedPawns:
        if promotedPawns[board[curPosition]] == 'b':
            return posBishopSquares(curPosition, color, board)
    if board[curPosition] in promotedPawns:
        if promotedPawns[board[curPosition]] == 'h':
            return posHorseSquares(curPosition, color, board)
    possibleMovement = []
    movementFactor = 1
    if color == "B":
        movementFactor = -1
    if len(lastPawn) > 0:
        if getTurn() - int(lastPawn[2]) == 1:
            if abs(lastPawn[1][0] - curPosition[0]) == 1 and lastPawn[1][1] == curPosition[1]:
                if (lastPawn[1][0], lastPawn[1][1] + movementFactor) not in board:
                    possibleMovement.append((lastPawn[1][0], lastPawn[1][1] + movementFactor))
    
    xPos = curPosition[0]
    yPos = curPosition[1]
    if pieceStats[board[curPosition]]["moved"] == False:
        if not (yPos + 2 * movementFactor > 8 or yPos + 2 * movementFactor < 1):
            if  ((xPos, yPos + 2 * movementFactor) not in board and (xPos, yPos +   movementFactor) not in board):
                possibleMovement.append((xPos, yPos + 2 * movementFactor))
    if not (yPos + movementFactor > 8 or yPos + movementFactor < 1):
        if not (xPos, yPos + movementFactor) in board:
            possibleMovement.append((xPos, yPos + movementFactor))
    if not ((yPos + movementFactor > 8 or yPos + movementFactor < 1) and (xPos + movementFactor > 8 or xPos + movementFactor < 1)):
        if (xPos + movementFactor, yPos + movementFactor) in board:
            if board[(xPos + movementFactor, yPos + movementFactor)][-1] != color:
                possibleMovement.append((xPos + movementFactor, yPos + movementFactor))
    if not ((yPos + movementFactor > 8 or yPos + movementFactor < 1) and (xPos - movementFactor > 8 or xPos - movementFactor < 1)):
        if (xPos - movementFactor, yPos + movementFactor) in board:
            if board[(xPos - movementFactor, yPos + movementFactor)][-1] != color:
                possibleMovement.append((xPos - movementFactor, yPos + movementFactor))




    return possibleMovement
def posBishopSquares(curPosition, color, board=Grid):
    xPos = curPosition[0]
    yPos = curPosition[1]
    possibleMovement =[]
    movement = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    for moves in movement:
        newXPos = xPos
        newYPos = yPos
        lineOfSight = False
        runnin = True
        while runnin:
            if  not (((newXPos + moves[0] > 8) or (newXPos + moves[0] < 1)) or ((newYPos + moves[1] > 8) or (newYPos + moves[1] < 1))):
                newXPos = newXPos + moves[0]
                newYPos = newYPos + moves[1]
                if lineOfSight == True:
                    runnin = False
                elif (newXPos, newYPos) not in board:
                    possibleMovement.append((newXPos, newYPos)) 
                elif board[(newXPos, newYPos)][-1] == color:
                    runnin = False
                elif board[(newXPos, newYPos)][-1] != color:
                    possibleMovement.append((newXPos, newYPos))
                    lineOfSight = True
                else:
                    possibleMovement.append((newXPos, newYPos))
            else:
                runnin = False
    return possibleMovement
def posRookSquares(curPosition, color, board=Grid):
    xPos = curPosition[0]
    yPos = curPosition[1]
    possibleMovement =[]
    onesArray = [-1, 1]
    #Xposition
    for one in onesArray:
        newXPos = xPos
        runnin = True
        lineOfSight = False
        while runnin:
            if  not ((newXPos + one > 8) or (newXPos + one < 1)):
                newXPos = newXPos + one
                if lineOfSight:
                    runnin = False 
                elif (newXPos, yPos) not in board:
                    possibleMovement.append((newXPos, yPos))     
                elif board[(newXPos, yPos)][-1] == color:
                    runnin = False
                elif board[(newXPos, yPos)][-1] != color:
                    possibleMovement.append((newXPos, yPos))
                    lineOfSight = True
                else:
                    possibleMovement.append((newXPos, yPos))
            else:
                runnin = False
    #Yposition
    for one in onesArray:
        newYPos = yPos
        runnin = True
        lineOfSight = False
        while runnin:
            if  not ((newYPos + one > 8) or (newYPos + one < 1)):
                newYPos = newYPos + one
                if lineOfSight == True:
                    runnin = False
                elif (xPos, newYPos) not in board:
                    possibleMovement.append((xPos, newYPos)) 
                elif board[(xPos, newYPos)][-1] == color:
                    runnin = False
                elif board[(xPos, newYPos)][-1] != color:
                    possibleMovement.append((xPos, newYPos))
                    lineOfSight = True
                else:
                    possibleMovement.append((xPos, newYPos))
            else:
                runnin = False
    return possibleMovement

def posQueenSquares(curPosition, color, board=Grid):
    possibleMovement = posRookSquares(curPosition, color, board)
    possibleMovement.extend(posBishopSquares(curPosition, color, board))
    return possibleMovement
def posKingSquares(curPosition, color, board=Grid):
    xPos = curPosition[0]
    yPos = curPosition[1]
    possibleMovement =[]
    for one in [-1, 0, 1]:
        newXPos = xPos + one
        for moves in [-1, 0, 1]:
            newYPos = yPos + moves
            if (newXPos, newYPos) == curPosition:
                continue
            if not (((newXPos > 8) or (newXPos < 1)) or ((newYPos > 8) or (newYPos < 1))):
                if (newXPos, newYPos) not in board:
                    possibleMovement.append((newXPos, newYPos))
                elif board[(newXPos, newYPos)][-1] == color:
                    continue
                elif board[(newXPos, newYPos)][-1] != color:
                    possibleMovement.append((newXPos, newYPos))
                else:
                    possibleMovement.append((newXPos, newYPos))
    if color == 'W':
        if (pieceStats["1k" + color]["moved"] == False) and (((pieceStats["1r" + color]["moved"] == False)) or (pieceStats["2r" + color]["moved"] == False)):
            if pieceStats["1r" + color]["moved"] == False and ((4, 1) not in board) and ((3, 1) not in board) and ((2, 1) not in board) and board[(1, 1)] == "1r" + color:
                possibleMovement.append((3, 1))
            if pieceStats["2r" + color]["moved"] == False and ((6, 1) not in board) and ((7, 1) not in board) and board[(8, 1)] == "2r" + color:
                possibleMovement.append((7, curPosition[1]))
    elif color == 'B':
        if (pieceStats["1k" + color]["moved"] == False) and (((pieceStats["1r" + color]["moved"] == False)) or (pieceStats["2r" + color]["moved"] == False)):
            if pieceStats["1r" + color]["moved"] == False and ((4, 8) not in board) and ((3, 8) not in board) and ((2, 8) not in board) and board[(1, 8)] == "1r" + color:
                possibleMovement.append((3, curPosition[1]))
            if pieceStats["2r" + color]["moved"] == False and ((6, 8) not in board) and ((7, 8) not in board) and board[(8, 8)] == "2r" + color:
                possibleMovement.append((7, curPosition[1]))

    return possibleMovement

def posPieceSquares (curPosition, board=Grid):
    piece = board[curPosition]
    if piece[1] == "h":
        return posHorseSquares(curPosition, piece[-1], board)
    elif piece[1] == "b":
        return posBishopSquares(curPosition, piece[-1], board)
    elif piece[1] == 'p':
        return posPawnSquares(curPosition, piece[-1], board)
    elif piece[1] == "r":
        return posRookSquares(curPosition, piece[-1], board)
    elif piece[1] == "k":
        return posKingSquares(curPosition, piece[-1], board)
    elif piece[1] == 'q':
        return posQueenSquares(curPosition, piece[-1], board)

def displayPossibleSquares(a):
    posSquares = pygame.Surface((100, 100))
    posSquares.set_alpha(150)
    posSquares.fill((135, 211, 255))
    for moves in a:
        screen.blit(posSquares, calculateCoordinatesFromGrid(moves))
        pygame.display.update()
def moveUpdate(pieceCoordinate, squarePosition, board=Grid, pieceStat=pieceStats, player=True):
    if "1k" in board[pieceCoordinate] and (squarePosition == (7, pieceCoordinate[1] ) and (pieceStats["1k" + Grid[pieceCoordinate][-1]]["moved"] == False)):
        pieceStat[board[pieceCoordinate]]["moved"] = True
        board[squarePosition] = board.pop(pieceCoordinate)
        board[(6, squarePosition[1])] = board.pop((8, squarePosition[1]))
    elif  "1k" in board[pieceCoordinate] and (squarePosition == (3, pieceCoordinate[1])) and (pieceStats["1k" + Grid[pieceCoordinate][-1]]["moved"] == False):
        pieceStat[board[pieceCoordinate]]["moved"] = True
        board[squarePosition] = board.pop(pieceCoordinate)
        board[(4, squarePosition[1])] = board.pop((1, squarePosition[1]))
    elif (board[pieceCoordinate][1:] == 'pW' and squarePosition[1] == 8) or (board[pieceCoordinate][1:] == 'pB' and squarePosition[1] == 1):
        pieceStat[board[pieceCoordinate]]["moved"] = True
        if player and pieceStats[board[pieceCoordinate]]["promotion"] == False:
            changeSceneToPromotion()
            pieceStat[board[pieceCoordinate]]["promoted"] = True
        board[squarePosition] = board.pop(pieceCoordinate)
    else:
        if player:
            if board[pieceCoordinate][1] == 'p':       
                if abs(pieceCoordinate[1] -   squarePosition[1]) == 2:
                    setLastPawn([getPreviousPiece(), getPreviousMove(), getTurn()])                 
        pieceStat[board[pieceCoordinate]]["moved"] = True
        if board[pieceCoordinate][1] == 'p' and pieceCoordinate[0] != squarePosition[0] and squarePosition not in board:
            movefac = -1
            if board[pieceCoordinate][2] == 'B':
                movefac = 1
            board.pop((squarePosition[0], squarePosition[1] + movefac))
        board[squarePosition] = board.pop(pieceCoordinate) 
    if player:
        itterateTurn()

def possibleMoves(currentTurn):
    global allPossibleMoves
    allPossibleMoves = {}
    for coordinate in Grid:
        if Grid[coordinate][-1] == currentTurn:
            allPossibleMoves[Grid[coordinate]] = []
            for move in posPieceSquares(coordinate):
                tempGrid = Grid.copy()
                tempPieceStats = copy.deepcopy(pieceStats)
                moveUpdate(pieceCoordinate=coordinate, squarePosition=move, board=tempGrid, pieceStat=tempPieceStats, player=False)
                for otherCoordinate in tempGrid:
                    breakLoop = False
                    if tempGrid[otherCoordinate][-1] != currentTurn:    
                        for squares in posPieceSquares(otherCoordinate, board=tempGrid):
                            if squares not in tempGrid:
                                appendIfEmpty(dicList=allPossibleMoves[Grid[coordinate]], move=move)
                            elif "1k" in tempGrid[squares]:
                                removeIfNotEmpty(dicList=allPossibleMoves[Grid[coordinate]], move=move)
                                breakLoop = True
                                break
                            else:
                                appendIfEmpty(dicList=allPossibleMoves[Grid[coordinate]], move=move)  
                    else:
                        continue
                    if breakLoop:
                        break
        else:
            continue
def allPossibleMoves():
    return allPossibleMoves
def checkCheckmate():
    global allPossibleMoves
    size = 0
    for moves in list(allPossibleMoves.values()):
        if len(moves) == 0:
            continue
        else:
            size = size + 1
    if size == 0:
        return True
    else:
        return False
def appendIfEmpty(dicList, move):
    if move not in dicList:
        dicList.append(move)

def removeIfNotEmpty(dicList, move):
    if move in dicList:
        dicList.remove(move)
def changeGrid(stuff):
    global Grid
    Grid = stuff
def changePawnState(clickPosition, board=Grid, ):
    global promotedPawns
    if clickPosition[1] == 4:
        if (clickPosition[0] == 3):
            promotedPawns[getPreviousPiece()] = 'q'
            pieceStats[getPreviousPiece()]['promotion'] = True
            setCurScene('')
            initPictures()
        elif (clickPosition[0] == 4):
            promotedPawns[getPreviousPiece()] = 'r'
            pieceStats[getPreviousPiece()]['promotion'] = True
            setCurScene('')
            initPictures()
        elif (clickPosition[0] == 5):
            promotedPawns[getPreviousPiece()] = 'b'
            pieceStats[getPreviousPiece()]['promotion'] = True
            setCurScene('')
            initPictures()
        elif (clickPosition[0] == 6):
            promotedPawns[getPreviousPiece()] = 'h'
            pieceStats[getPreviousPiece()]['promotion'] = True
            setCurScene('')
            initPictures()
def getPreviousPiece():
    return previousPiece
def setPreviousPiece(value):
    global previousPiece
    previousPiece = value
def getPreviousMove():
    return previousMove
def setPreviousMove(value):
    global previousMove
    previousMove = value
def setLastPawn(val):
    global lastPawn
    lastPawn = val
def getLastPawn():
    return lastPawn

