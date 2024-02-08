import pygame
from chessPiecesInnit import *
from chessPiecesMovement import *
from game import *
from time import sleep
pygame.init()
icon = pygame.image.load('chessIcon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Chess')
initGrid()
initPictures()
possibleMoves(currentTurn=currentTurn())

while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif getCurScene() == 'promotion':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.dict["button"] == 1):
                    changePawnState(clickPosition=calculatePositionByClick(pygame.mouse.get_pos()))
                    possibleMoves(currentTurn())                  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (event.dict["button"] == 1):
                print(calculatePositionByClick(pygame.mouse.get_pos()))
                if calculatePositionByClick(pygame.mouse.get_pos()) in selectCoords:
                    setPreviousPiece(Grid[pieceCoordinate])
                    setPreviousMove(calculatePositionByClick(pygame.mouse.get_pos()))
                    moveUpdate(pieceCoordinate=pieceCoordinate, squarePosition=calculatePositionByClick(pygame.mouse.get_pos()))
                    initPictures()
                    pygame.display.update()

                    pieceCoordinate = None
                    selectCoords = []
                    if getCurScene() == 'promotion':
                        initPromotion()
                        pygame.display.update()  
                    switchTurn()
                    possibleMoves(currentTurn())
                    continue
                if (calculatePositionByClick(pygame.mouse.get_pos()) in Grid):
                    print(Grid[calculatePositionByClick(pygame.mouse.get_pos())])
                    if (pieceCoordinate == None or pieceCoordinate != calculatePositionByClick(pygame.mouse.get_pos()) ) and Grid[calculatePositionByClick(pygame.mouse.get_pos())][-1] == currentTurn():
                        initPictures()
                        pieceCoordinate = calculatePositionByClick(pygame.mouse.get_pos())
                        selectCoords = allPossibleMoves()[Grid[calculatePositionByClick(pygame.mouse.get_pos())]]
                        displayPossibleSquares(selectCoords)
        elif event.type == pygame.KEYUP:
            if event.dict['unicode'] == 'z':
                pass
        elif checkCheckmate():
            sleep(5)
            pygame.quit()
    clock.tick(30)
pygame.quit()

