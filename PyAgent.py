# PyAgent.py
import random
from enum import Enum

import Action
import Orientation

class knowledge(Enum):
    Unkown = 0
    Safe = 1
    Stench = 2
    PossibleWumpus = 3
    Wumpus = 4

x = 1
y = 1
gold = False
arrow = True
orientation = Orientation.RIGHT
width = None
height = None
knowledgeBase = {}
visited = {}
wumpusFound = False
wumpusLocation = None
possibleWumpuses = []
bufferedRoute = []
pathHomeIndex = 0
endingOrientation = None
playingAgain = None
shootAgain = None
goldLoc = None

def PyAgent_Constructor ():
    print("PyAgent_Constructor")

def PyAgent_Destructor ():
    print("PyAgent_Destructor")

def PyAgent_Initialize ():
    print("PyAgent_Initialize")
    global x,y,gold,arrow,orientation, endingOrientation, pathHomeIndex, playingAgain

    print("GoldGG", gold, bufferedRoute)
    x = 1
    y = 1
    gold = False
    arrow = True
    endingOrientation = orientation
    orientation = Orientation.RIGHT

    if playingAgain is False:
        playingAgain = True

    if playingAgain is None:
        playingAgain = False

    print("@@Playing again ", playingAgain)

def getPrevLocation():
    global x, y
    prevX = x
    prevY = y
    if orientation % 4 is Orientation.RIGHT:
        prevX-=1
    elif orientation % 4 is Orientation.LEFT:
        prevX+=1
    elif orientation % 4 is Orientation.UP:
        prevY-=1
    elif orientation % 4 is Orientation.DOWN:
        y+= 1
    return prevX, prevY

def getLocationInfront():
    global x, y
    nextX = x
    nextY = y
    if orientation is Orientation.RIGHT:
        nextX += 1
    elif orientation is Orientation.LEFT:
        nextX -= 1
    elif orientation is Orientation.UP:
        nextY += 1
    elif orientation is Orientation.DOWN:
        nextY -= 1

    return nextX, nextY

def getNeighbors(location):
    x,y = location
    return [(x+1, y), (x,y+1), (x,y-1), (x-1,y)]

def inBounds(location):
    x,y = location
    return x > 0 and (width is None or x <= width) and y > 0 and (height is None or y <= height)

def willBump(x, y):
    global width, height
    if width is not None and x > width:
        return True
    elif height is not None and y > height:
        return True
    else:
        return False

def wumpusPlausible(location):
    global knowledgeBase
    x,y = location

    if location in knowledgeBase.keys() and knowledgeBase[location] is knowledge.Wumpus:
        return True

    for neighbor in getNeighbors((x,y)):
        if inBounds(neighbor) and neighbor in visited.keys() and knowledgeBase[neighbor] is knowledge.Safe:
            print("No wumpus in ", location)
            return False

    return True

def getCommandsToFaceLeft(orientation):
    if orientation == Orientation.RIGHT:
        return [Action.TURNRIGHT, Action.TURNRIGHT]
    elif orientation == Orientation.LEFT:
        return []
    elif orientation == Orientation.DOWN:
        return [Action.TURNRIGHT]
    else:
        return [Action.TURNLEFT]

def getCommandsToFaceRight(orientation):
    if orientation == Orientation.LEFT:
        return [Action.TURNRIGHT, Action.TURNRIGHT]
    elif orientation == Orientation.RIGHT:
        return []
    elif orientation == Orientation.UP:
        return [Action.TURNRIGHT]
    else:
        return [Action.TURNLEFT]

def getCommandsToFaceDown(orientation):
    if orientation is Orientation.UP:
        return [Action.TURNRIGHT, Action.TURNRIGHT]
    elif orientation is Orientation.DOWN:
        return []
    elif orientation is Orientation.LEFT:
        return [Action.TURNLEFT]
    else:
        return [Action.TURNRIGHT]

def getCommandsToFaceUp(orientation):
    if orientation is Orientation.DOWN:
        return [Action.TURNRIGHT, Action.TURNRIGHT]
    elif orientation is Orientation.UP:
        return []
    elif orientation is Orientation.RIGHT:
        return [Action.TURNLEFT]
    else:
        return [Action.TURNRIGHT]

def getCommandsToFace(curOrientation, desiredOrientation):
    if desiredOrientation is Orientation.UP:
        return getCommandsToFaceUp(curOrientation)
    if desiredOrientation is Orientation.DOWN:
        return getCommandsToFaceDown(curOrientation)
    if desiredOrientation is Orientation.RIGHT:
        return getCommandsToFaceRight(curOrientation)
    if desiredOrientation is Orientation.LEFT:
        return getCommandsToFaceLeft(orientation)

def leftOrDownTieBreaker():
    if x == 1:
        return True, False

    if y == 1:
        return False, True

    if orientation is Orientation.UP or orientation is Orientation.LEFT:
        return True, False
    else:
        return False, True


def forwardToBump(direction):
    result = [Action.GOFORWARD]

    timesForward = 0

    if direction is Orientation.LEFT:
        result *= x-1

    elif direction is Orientation.DOWN:
        result *= y-1

    else:
        result = []


    print("RESULT!", result)

    return result


def planRouteHome():
    global wumpusFound, wumpusLocation, x,y

    if not wumpusFound:
        wumpusLocation = (x+2, y+2)

    #Go down if the wumpus is in the first column and we will run into the wumpus, or if the wumpus is not in our column
    goDown = (wumpusLocation[0] == 1 and wumpusLocation[1] <= y) or wumpusLocation[1] > y or wumpusLocation[0] != x


    #Go left if the wumpus is in the first row and we will run into the wumpus, or if the wumpus is not in our row
    goLeft = (wumpusLocation[1] == 1 and wumpusLocation[0] <= x) or wumpusLocation[0] > x or wumpusLocation[1] != y

    global bufferedRoute

    if goLeft and goDown:
        goLeft, goDown = leftOrDownTieBreaker()

    if goDown:
        print("Going down")
        bufferedRoute += getCommandsToFaceDown(orientation)
        bufferedRoute += forwardToBump(Orientation.DOWN)
        bufferedRoute += getCommandsToFaceLeft(Orientation.DOWN)
        bufferedRoute += forwardToBump(Orientation.LEFT)
        bufferedRoute.append(Action.CLIMB)
        print(bufferedRoute)
    elif goLeft:
        print("GOing left")
        bufferedRoute += getCommandsToFaceLeft(orientation)
        bufferedRoute += forwardToBump(Orientation.LEFT)
        bufferedRoute += getCommandsToFaceDown(Orientation.LEFT)
        bufferedRoute += forwardToBump(Orientation.DOWN)
        bufferedRoute.append(Action.CLIMB)

    else:
        #We can't get home because we are on the left or on the bottom and the path is blocked
        if x == 1:
            #On the bottom
            bufferedRoute += getCommandsToFaceUp(orientation)
            bufferedRoute.append(Action.GOFORWARD)
            bufferedRoute += getCommandsToFaceLeft(Orientation.UP)
            bufferedRoute += forwardToBump(Orientation.LEFT)
            bufferedRoute += getCommandsToFaceDown(Orientation.LEFT)
            bufferedRoute += forwardToBump(Orientation.DOWN)
            bufferedRoute += [Action.GOFORWARD, Action.CLIMB]

        if y == 1:
            #On the left
            bufferedRoute += getCommandsToFaceRight(orientation)
            bufferedRoute.append(Action.GOFORWARD)
            bufferedRoute += getCommandsToFaceDown(Orientation.RIGHT)
            bufferedRoute += forwardToBump(Orientation.DOWN)
            bufferedRoute += getCommandsToFaceLeft(Orientation.DOWN)
            bufferedRoute += forwardToBump(Orientation.LEFT)
            bufferedRoute += [Action.GOFORWARD, Action.CLIMB]

        #Wumpus not found
        #TODO


def locationSafeAndUnexplored(nextLocation):
    global knowledgeBase
    return nextLocation not in visited.keys() and (nextLocation not in knowledgeBase.keys() or knowledgeBase[nextLocation] is knowledge.Safe or knowledgeBase[nextLocation] is knowledge.PossibleWumpus and wumpusFound)


def turn(action):
    if action is Action.TURNRIGHT:
        return turnRight()
    elif action is Action.TURNLEFT:
        return turnLeft()
    else:
        print("Trying to turn with non turn action", action)
        exit(1)



def turnRight():
    global orientation
    orientation = (orientation - 1) % 4
    return Action.TURNRIGHT

def turnLeft():
    global orientation
    orientation = (orientation + 1) % 4
    return Action.TURNLEFT

# Only use this on neighbors
def facePoint(otherLocation):
    otherX,otherY = otherLocation
    global orientation
    if x < otherX:
        if orientation is Orientation.DOWN:
            return turnLeft()
        else:
            return turnRight()
    elif x > otherX:
        if orientation is Orientation.UP:
            return turnLeft()
        else:
            return turnRight()

    elif y < otherY:
        if orientation is Orientation.LEFT:
            return turnRight()
        else:
            return turnLeft()
    elif y > otherY:
        if orientation is Orientation.LEFT:
            return turnLeft()
        else:
            return turnRight()

def getOppositeTurn(turn):
    if turn == Action.TURNLEFT:
        return turnRight()
    if turn == Action.TURNRIGHT:
        return turnLeft()
    else:
        print("Can't unturn a non turn")
        exit(1)

def getOppositeDirection(direction):
    if direction is Orientation.RIGHT:
        return Orientation.LEFT
    if direction is Orientation.LEFT:
        return Orientation.RIGHT
    if direction is Orientation.UP:
        return Orientation.DOWN
    if direction is Orientation.DOWN:
        return  Orientation.UP

def goForward():
    global x,y, orientation
    if orientation is Orientation.RIGHT:
        x += 1

    if orientation is Orientation.LEFT:
        x -= 1

    if orientation is Orientation.UP:
        y += 1

    if orientation is Orientation.DOWN:
        y -= 1

    return Action.GOFORWARD



def PyAgent_Process (stench,breeze,glitter,bump,scream):
    # time.sleep(1)

    global x, y, orientation, width, height, gold, knowledgeBase, pathHomeIndex, bufferedRoute, arrow, visited, goldLoc

    perceptStr = ""
    if (stench == 1):
        perceptStr += "Stench=True,"
    else:
        perceptStr += "Stench=False,"
    if (breeze == 1):
        perceptStr += "Breeze=True,"
    else:
        perceptStr += "Breeze=False,"
    if (glitter == 1):
        perceptStr += "Glitter=True,"
    else:
        perceptStr += "Glitter=False,"
    if (bump == 1):
        perceptStr += "Bump=True,"
    else:
        perceptStr += "Bump=False,"
    if (scream == 1):
        perceptStr += "Scream=True"
    else:
        perceptStr += "Scream=False"
    print("PyAgent_Process: " + perceptStr + '\n', x, y, gold, arrow, orientation, width, height, wumpusLocation)

    if x == 1 and y == 1 and gold:
        global endingOrientation
        endingOrientation = orientation
        return Action.CLIMB

    if playingAgain:
        print("Playing again!")
        if goldLoc is not None:
            global shootAgain
            if scream:
                shootAgain = True
            if not arrow and shootAgain is None:
                shootAgain = False

            if not gold:
                if x < goldLoc[0]:
                    toFaceRight = getCommandsToFaceRight(orientation)
                    if len(toFaceRight) > 0:
                        return turn(toFaceRight[0])

                    if stench and arrow:
                        arrow = False
                        return Action.SHOOT
                    return goForward()

                if y < goldLoc[1]:
                    toFaceup = getCommandsToFaceUp(orientation)
                    if len(toFaceup) > 0:
                        return turn(toFaceup[0])

                    if stench and arrow and (shootAgain is None or shootAgain):
                        arrow = False
                        return Action.SHOOT
                    return goForward()

                if glitter:
                    gold = True
                    return Action.GRAB
                else:
                    print("Error, no action to execute")

            else:
                if y > 1:
                    commands = getCommandsToFaceDown(orientation)
                    if len(commands) > 0:
                        return turn(commands[0])

                    return goForward()

                if x > 1:
                    commands = getCommandsToFaceLeft(orientation)
                    if len(commands) > 0:
                        print("going to Facing left")
                        print(commands)
                        return turn(commands[0])
                    return goForward()

                return Action.CLIMB
        else:
            print("Playing again after not finding gold")
            pass

    if bump is 1:
        if orientation is Orientation.RIGHT:
            x -= 1
            if width is None:
                width = x

        if orientation is Orientation.LEFT:
            x += 1

        if orientation is Orientation.UP:
            y -= 1
            if height is None:
                height = y

        if orientation is Orientation.DOWN:
            y += 1

    print(knowledgeBase, "\n")
    print(visited, "\n")


    if glitter is 1:
        gold = True
        planRouteHome()
        global goldLoc
        goldLoc = (x,y)
        return Action.GRAB

    if gold:
        print("On buffered route: ", pathHomeIndex, bufferedRoute)
        action = bufferedRoute[pathHomeIndex]
        if action is Action.GOFORWARD:
            nextLocation = getLocationInfront()
            if wumpusPlausible(nextLocation) and arrow:
                arrow = False
                return Action.SHOOT
            pathHomeIndex+=1
            return goForward()
        else:
            turnAction = bufferedRoute[pathHomeIndex]
            pathHomeIndex+=1
            return turn(turnAction)

    nextLocation = getLocationInfront()

    xSaved = x
    ySaved = y

    UpdateKnowledgeBase(stench, xSaved, ySaved)
    nextMove = PickNextMove(knowledgeBase, nextLocation, x, y)
    print("PICK NEXT MOVE", nextMove)
    return nextMove


def PickNextMove(knowledgeBase, nextLocation, x, y):
    if inBounds(nextLocation) and locationSafeAndUnexplored(nextLocation):
        # Explore directly in front of us
        return goForward()
    else:
        neighbors = getNeighbors((x, y))
        print("NAAYBORES", neighbors)
        for neighbor in neighbors:
            if inBounds(neighbor) and (locationSafeAndUnexplored(neighbor)):
                print("Found neighbor")
                return facePoint(neighbor)

        # If we reach this point, no neighbor is unexplored and safe, we will pick a safe direction

        print("No unvisited safe neighbor")


        safeNeighbors = []
        for neighbor in neighbors:
            if inBounds(neighbor) and (neighbor in visited.keys() or neighbor in knowledgeBase.keys() and knowledgeBase[neighbor] is knowledge.Safe):
                safeNeighbors.append(neighbor)
            else:
                print(neighbor, "Not safe")

        if nextLocation in safeNeighbors:
            safeNeighbors += [nextLocation] * 1

        print(safeNeighbors)

        if len(safeNeighbors) == 0:
            return goForward()

        face = random.randrange(len(safeNeighbors))

        nextTarget = safeNeighbors[face]

        if nextTarget is nextLocation:
            return goForward()
        else:
            return facePoint(nextTarget)


def UpdateKnowledgeBase(stench, x, y):
    global knowledgeBase
    if stench == 1:
        knowledgeBase[(x, y)] = knowledge.Stench

        print("XXX set stench", (x,y))

        neighbors = getNeighbors((x, y))

        possibleWumpusCount = 0
        possibleWumpus = (-1,-1)

        for neighbor in neighbors:
            if neighbor in possibleWumpuses and (x,y) not in visited.keys():
                global wumpusFound, wumpusLocation
                wumpusFound = True
                wumpusLocation = neighbor
                knowledgeBase[wumpusLocation] = knowledge.Wumpus
                print("FOund wumpus at ", wumpusLocation)
                visited[(x,y)] = True
                return

        visited[(x,y)] = True

        for neighbor in neighbors:
            if inBounds(neighbor) and wumpusPlausible(neighbor):
                possibleWumpusCount += 1
                possibleWumpus = neighbor
                # if true, then we are adding a new possible wumpus
                if neighbor not in knowledgeBase.keys():
                    possibleWumpuses.append(neighbor)
                knowledgeBase[neighbor] = knowledge.PossibleWumpus

        if possibleWumpusCount == 1:
            # Only one possible spot for the wumpus to be, therefore we have found it.
            global wumpusFound, wumpusLocation
            wumpusFound = True
            wumpusLocation = possibleWumpus
            knowledgeBase[wumpusLocation] = knowledge.Wumpus
            print("FOund wumpus at ", wumpusLocation)
            return

    else:
        visited[(x,y)] = True
        knowledgeBase[(x,y)] = knowledge.Safe
        if (x, y) in knowledgeBase.keys() and knowledgeBase[(x, y)] is knowledge.PossibleWumpus:
            possibleWumpuses.remove((x, y))
            knowledgeBase[(x, y)] = knowledge.Safe

            toRemove = []

            for possibleWumpus in possibleWumpuses:
                if not wumpusPlausible(possibleWumpus):
                    toRemove.append()

            for nonWumpus in toRemove:
                possibleWumpuses.remove(nonWumpus)

            if len(possibleWumpuses) == 1:
                global wumpusFound
                wumpusFound = True
                wumpusLocation = possibleWumpuses[0]

        else:
            knowledgeBase[(x, y)] = knowledge.Safe
            for neighbor in getNeighbors((x, y)):
                if inBounds(neighbor):
                    if neighbor not in knowledgeBase.keys():
                        knowledgeBase[neighbor] = knowledge.Safe
                    elif knowledgeBase[neighbor] is knowledge.PossibleWumpus:
                        possibleWumpuses.remove(neighbor)

                    if knowledgeBase[neighbor] is not knowledge.Stench:
                        knowledgeBase[neighbor] = knowledge.Safe


def PyAgent_GameOver (score):
    print("PyAgent_GameOver: score = " + str(score))
