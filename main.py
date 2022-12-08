import grid as g
import player as p
from tkinter import *
from PIL import Image
from functools import partial
import shutil


def count(mainCount):
    if mainCount == 0:
        shutil.rmtree('pieces/blue')
        shutil.rmtree('pieces/piecesX2/pieces/blue')
        shutil.copytree('pieces/Start/blue', 'pieces/blue')
        shutil.copytree('pieces/Start/pieces/blue', 'pieces/piecesX2/pieces/blue')
        shutil.rmtree('pieces/red')
        shutil.rmtree('pieces/piecesX2/pieces/red')
        shutil.copytree('pieces/Start/red', 'pieces/red')
        shutil.copytree('pieces/Start/pieces/red', 'pieces/piecesX2/pieces/red')
        shutil.rmtree('pieces/yellow')
        shutil.rmtree('pieces/piecesX2/pieces/yellow')
        shutil.copytree('pieces/Start/yellow', 'pieces/yellow')
        shutil.copytree('pieces/Start/pieces/yellow', 'pieces/piecesX2/pieces/yellow')
        shutil.rmtree('pieces/green')
        shutil.rmtree('pieces/piecesX2/pieces/green')
        shutil.copytree('pieces/Start/green', 'pieces/green')
        shutil.copytree('pieces/Start/pieces/green', 'pieces/piecesX2/pieces/green')
    return mainCount + 1


def takeCoord(event):
    global player
    global counter
    global roundGame

    x = int((event.x - jeu.offsetX) / sizeCells)
    y = int((event.y - jeu.offsetY) / sizeCells)
    informations.create_text(329, 230, text=x)
    informations.create_text(329, 240, text=y)

    if available(x, y):

        player.putPiece(piece - 1, (x, y))
        player.removePiece(piece)
        if counter == 0 and player1.surrend != True:
            player = player1
            counter += 1
        elif counter == 1 and player2.surrend != True:
            player = player2
            counter += 1
        elif counter == 2 and player3.surrend != True:
            player = player3
            counter += 1
        elif counter == 3 and player4.surrend != True:
            player = player4
            counter = 0
            roundGame += 1

        jeu.updateGridTk(game)
        availablePiecesDisplay()


def modifPiece(event):
    if event.keysym == 'r':
        player.rotationPieces(piece)
        image = Image.open(player.namePieceListImg[piece])
        imRotate = image.rotate(-90)
        imRotate.save(player.namePieceListImg[piece])
        image = Image.open("pieces/piecesX2/{}".format(player.namePieceListImg[piece]))
        imRotate = image.rotate(-90)
        imRotate.save("pieces/piecesX2/{}".format(player.namePieceListImg[piece]))
    if event.keysym == 's':
        player.symmetryPieces(piece)
        image = Image.open(player.namePieceListImg[piece])
        imFlip = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        imFlip.save(player.namePieceListImg[piece])
        image = Image.open("pieces/piecesX2/{}".format(player.namePieceListImg[piece]))
        imFlip = image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
        imFlip.save("pieces/piecesX2/{}".format(player.namePieceListImg[piece]))


def available(x, y):
    inAngle = False

    beginningTurn = False

    nextToColor = False

    # Beginning or not ?
    if len(player.namePieceList) == 21:
        beginningTurn = True

    # Check multiple condition of each part of the piece
    for cell in player.pieceToCoord()[piece - 1]:
        cellX, cellY = cell

        # Piece is outside the box or on another piece or not available?
        if x + cellX - 2 > jeu.numberCells - 1 or \
                y + cellY - 2 > jeu.numberCells - 1 or \
                x + cellX - 2 < 0 or y + cellY - 2 < 0 or \
                jeu.arrayGrid[x + cellX - 2][y + cellY - 2] != 0 or \
                piece not in player.namePieceList:
            informations.create_text(329, 250, text='Impossible')
            print('Piece is outside the box or on another piece or not available')
            return False

        # Part of the piece is in the angle at the beginning ?
        if beginningTurn and \
                ((x + cellX - 2, y + cellY - 2) == (0, 0) or
                 (x + cellX - 2, y + cellY - 2) == (0, 19) or
                 (x + cellX - 2, y + cellY - 2) == (19, 0) or
                 (x + cellX - 2, y + cellY - 2) == (19, 19)):
            inAngle = True
            print('Part of the piece is in the angle at the beginning')

        # Piece is too attached to his color ?
        if not beginningTurn and \
                (x + cellX - 2 != 0 and jeu.arrayGrid[x + cellX - 2 - 1][y + cellY - 2] == player.initial or
                 x + cellX - 2 != 19 and jeu.arrayGrid[x + cellX - 2 + 1][y + cellY - 2] == player.initial or
                 y + cellY - 2 != 0 and jeu.arrayGrid[x + cellX - 2][y + cellY - 2 - 1] == player.initial or
                 y + cellY - 2 != 19 and jeu.arrayGrid[x + cellX - 2][y + cellY - 2 + 1] == player.initial):
            informations.create_text(329, 250, text='Impossible')
            print('Piece is too attached to his color')
            return False

        # Part of the piece is next to his color ?
        if not beginningTurn and \
                (x + cellX - 2 != 0 and y + cellY - 2 != 0 and
                 jeu.arrayGrid[x + cellX - 2 - 1][y + cellY - 2 - 1] == player.initial) or \
                (x + cellX - 2 != 19 and y + cellY - 2 != 0 and
                 jeu.arrayGrid[x + cellX - 2 + 1][y + cellY - 2 - 1] == player.initial) or \
                (x + cellX - 2 != 0 and y + cellY - 2 != 19 and
                 jeu.arrayGrid[x + cellX - 2 - 1][y + cellY - 2 + 1] == player.initial) or \
                (x + cellX - 2 != 19 and y + cellY - 2 != 19 and
                 jeu.arrayGrid[x + cellX - 2 + 1][y + cellY - 2 + 1] == player.initial):
            nextToColor = True
            print('Part of the piece is next to his color')

    # Piece is in the angle at the beginning ?
    if beginningTurn and not inAngle:
        informations.create_text(329, 250, text='Le 1er tour est au niveau des angles')
        print("Piece is in the angle at the beginning")
        return False

    # Piece is next to his color ?
    if not beginningTurn and not nextToColor:
        print("Piece is next to his color")
        return False

    return True


def pieceFollowing(event):
    x, y = event.x, event.y
    global piece

    try:
        fileImg = "pieces/piecesX2/{}".format(player.namePieceListImg[piece])
        img = PhotoImage(file=fileImg)
        temp[fileImg] = img
        img = game.create_image(-330, -330, image=img, anchor='nw')

        if x > 830 or x < 30 or y > 830 or y < 30:
            '''availablePiecesDisplay()'''
        else:
            jeu.updateGridTk(game)
            x = int((event.x - jeu.offsetX) / sizeCells)
            y = int((event.y - jeu.offsetY) / sizeCells)
            game.coords(img, x * 40 - 50, y * 40 - 50)
    except:
        print("")


def availablePiecesDisplay():
    oX = 60
    oY = 300
    space = 10

    informations = Canvas(window, width=658, height=860)
    informations.grid(row=0, column=1)

    for i in range(5):
        for j in range(5):
            if i < 4 or (i == 4 and j == 2):
                if i * 5 + j + 1 <= 20:
                    num = i * 5 + j + 1
                else:
                    num = 21

                if num in player.namePieceList:
                    fileImg = player.namePieceListImg[num]
                    img = PhotoImage(file=fileImg)
                    temp[fileImg] = img
                    informations.create_image(oX + (100 + space) * j, oY + (100 + space) * i, image=img, anchor='nw')
                    btn = Button(informations, image=img, command=partial(selectionPiece, num))
                    btn.place(x=oX + (100 + space) * j, y=oY + (100 + space) * i)


def selectionPiece(num):
    global piece
    piece = num
    informations.create_text(329, 200, text=num)
    availablePiecesDisplay()


mainCount = 0
mainCount = count(mainCount)

piece = 1
numberCells = 20
sizeCells = 40
turn = 0
offsetX = 30
offsetY = 30

temp = {}

jeu = g.Grid(offsetX, offsetY, sizeCells, [], numberCells)

window = Tk()
window.title("Blokus")
window.attributes('-fullscreen', True)

game = Canvas(window, width=870, height=860)

game.grid(row=0, column=0)
game.create_rectangle(offsetX, offsetY, 830, 830)
game.create_line(871, 0, 871, 860, width=2)

informations = Canvas(window, width=658, height=860)
informations.grid(row=0, column=1)

jeu.creationGridTk(game)

player1 = p.Player("blue", "B", jeu)
player2 = p.Player("red", "R", jeu)
player3 = p.Player("yellow", "Y", jeu)
player4 = p.Player("green", "G", jeu)
player = player1
counter = 1
roundGame = 0

availablePiecesDisplay()

game.bind('<Button-1>', takeCoord)

window.bind('<Escape>', lambda e: window.destroy())
window.bind('<Key>', modifPiece)

game.bind('<Motion>', pieceFollowing)

window.mainloop()
