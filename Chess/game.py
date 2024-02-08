turn = 1
playerturn = "W"
inCheck = False
selectCoords = []
pieceCoordinate = None
curScene = ''
def switchTurn():
    global playerturn
    if playerturn == "W":
        playerturn = "B"
    else:
        playerturn = "W"
def currentTurn ():
    return playerturn
def changeSceneToPromotion():
    global curScene
    curScene = 'promotion'
def getCurScene():
    return curScene
def setCurScene(value):
    global curScene
    curScene = value
def itterateTurn():
    global turn
    turn = turn + 1
def getTurn():
    global turn
    return turn