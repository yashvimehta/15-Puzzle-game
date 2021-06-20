import turtle
from turtle import *
from tkinter import *
import tkinter as tk
import random
import sys
from copy import copy, deepcopy
from tkinter import messagebox
import time
from PIL import ImageTk
from playsound import playsound

NUM_ROWS = 4  # Max 4
NUM_COLS = 4  # Max 4
TILE_WIDTH = 90  # Actual image size
TILE_HEIGHT = 90  # Actual image size
FONT_SIZE = 24
FONT = ('Helvetica', FONT_SIZE, 'normal')
SCRAMBLE_DEPTH = 30
row = [ 1, 0, -1, 0 ];
col = [ 0, -1, 0, 1 ];
counterWindow=0 # keep track of window
finalCount=0 #
steps=-1 # to calculate no of steps of user

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
  
    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
  
    # for popping an element based on Priority
    def delete(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                #print(self.queue[i].cost)
                if self.queue[i].cost +self.queue[i].level < self.queue[min].cost +self.queue[i].level:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()

class Node: 
    def __init__(self,mat, x, y, level, parent):
        self.parent=parent
        self.mat=mat
        self.x=x
        self.y=y
        self.cost=sys.maxsize
        self.level=level
        self.child=[]

def newNode(mat, x, y, newX, newY , level, parent):
    arr = deepcopy(mat)
    node = Node(arr, x, y , level, parent);
    temp=node.mat[x][y]
    node.mat[x][y] = node.mat[newX][newY]
    node.mat[newX][newY]=temp
    node.x = newX;
    node.y = newY;
    return node;

def calculateCost(initial, final):
    count = 0;
    for i in range(4):
        for j in range(4):
            if(initial[i][j] and initial[i][j] !=final[i][j] ):
                count=count+1
    return count;

def isSafe(x, y):
    return (x >= 0 and x < 4 and y >= 0 and y < 4);

def printMatrix(mat):
    global solutions
    matrix=[]
    for i in range(4):
        for j in range(4):
            print(mat[i][j],end=" ")
            matrix.append(mat[i][j])
        print()
    solutions.append(matrix)

def printPath(root):
    if (root == None):
        return;
    printPath(root.parent);
    printMatrix(root.mat);
    print();


def register_images():
    global screen
    for i in range(len(images)):
        screen.addshape(images[i])


def index_2d(my_list, v):
    # Returns the position of an element in a 2D list.
    for i, x in enumerate(my_list):
        if v in x:
            return (i, x.index(v))


def swap_tile(tile):
    # Swaps the position of the clicked tile with the empty tile.
    global screen,board,titlee ,steps, scramble
    current_i, current_j = index_2d(board, tile)
    empty_i, empty_j = find_empty_square_pos()
    empty_square = board[empty_i][empty_j]
  
    if is_adjacent([current_i, current_j], [empty_i, empty_j]):
        temp = board[empty_i][empty_j]
        board[empty_i][empty_j] = tile
        board[current_i][current_j] = temp        
        
        if(steps>=0 and scramble==True):
            steps=steps+1
            titlee.clear()
            titlee.write("Steps : %d"%steps,align="center", font=("Times New Roman",20, "normal", 'bold'))
            playsound('drumstick.wav')

        draw_board()


def is_adjacent(el1, el2):
    # Determines whether two elements in a 2D array are adjacent.
    if abs(el2[1] - el1[1]) == 1 and abs(el2[0] - el1[0]) == 0:
        return True
    if abs(el2[0] - el1[0]) == 1 and abs(el2[1] - el1[1]) == 0:
        return True
    return False


def find_empty_square_pos():
    # Returns the position of the empty square.
    global board
    for row in board:
        for candidate in row:
            if candidate.shape() == "number-images/empty.gif":
                empty_square = candidate

    return index_2d(board, empty_square)


def scramble_board():
    # Scrambles the board in a way that leaves it solvable.
    global board, screen , finalCount, scramble
    scramble=False
    k=1
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if(k!=16):
                board[i][j].shape("number-images/"+str(k)+".gif")
            else:
                board[i][j].shape("number-images/empty.gif")
            k=k+1


    for i in range(SCRAMBLE_DEPTH):
        finalCount=0
        for row in board:
            for candidate in row:
                if candidate.shape() == "number-images/empty.gif":
                    empty_square = candidate

        directions = ["up", "down", "left", "right"]
        empty_i, empty_j = find_empty_square_pos()

        if empty_i == 0: directions.remove("up")
        if empty_i >= NUM_ROWS - 1: directions.remove("down")
        if empty_j == 0: directions.remove("left")
        if empty_j >= NUM_COLS - 1: directions.remove("right")


        direction = random.choice(directions)

        if direction == "up": 
            swap_tile(board[empty_i - 1][empty_j])
        if direction == "down":
            swap_tile(board[empty_i + 1][empty_j])
        if direction == "left": 
            swap_tile(board[empty_i][empty_j - 1])
        if direction == "right": 
            swap_tile(board[empty_i][empty_j + 1])
        prev=direction
    solutions.clear()
    finalCount=finalCount+1
    return solution()


def draw_board():
    global screen, board , finalCount, start_time , timee

    # Disable animation
    screen.tracer(0)

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile = board[i][j]
            tile.goto(-138 + j * (TILE_WIDTH + 2), 138 - i * (TILE_HEIGHT + 2))

    # Restore animation
    screen.tracer(1)
    p=0# to find if it has reached final state
    i=0
    for s in board:
        for candidate in s:
            file = f"number-images/{i+1}.gif"
            # print(file)
            if(file=="number-images/16.gif"):
                file="number-images/empty.gif"
            if(candidate.shape()!=file):
                p=p+1
            i=i+1
    if(p==0 and finalCount!=0):
        timee=time.time()-start_time
        main2()


def create_tiles():
    # Creates and returns a 2D list of tiles based on turtle objects in the winning configuration.
    board = [["#" for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile_num = NUM_COLS * i + j
            tile = turtle.Turtle(images[tile_num])
            tile.penup()
            board[i][j] = tile

            def click_callback(x, y, tile=tile):
                """Passes `tile` to `swap_tile()` function."""
                return swap_tile(tile)

            tile.onclick(click_callback)

    return board


def getChild(min):
    cost=sys.maxsize
    item=None
    for i in range(len(min.child)):
        if(min.child[i].cost<cost):
            cost=min.child[i].cost
            item=min.child[i]
    return item

def solution():
    global initialBoard
    matList=[]
    initialBoard = [[0 for c in range(4)] for r in range(4)]
    empty_i, empty_j = find_empty_square_pos()
    initialBoard[empty_i][empty_j]=0;
    x,y=find_empty_square_pos();
    counter=1
    finalBoard = [[0 for c in range(4)] for r in range(4)]
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            if(counter==16):
                finalBoard[i][j]=0
            else:
                finalBoard[i][j]=counter
                counter=counter+1

    i=0
    j=0
    for s in board:
        if(i<=3):
            for candidate in s:
                if(j<=3):
                    if candidate.shape()=="number-images/empty.gif":
                        initialBoard[i][j]=0
                    elif candidate.shape()=="number-images/10.gif" or candidate.shape()=="number-images/11.gif" or candidate.shape()=="number-images/12.gif" or candidate.shape()=="number-images/13.gif" or candidate.shape()=="number-images/14.gif" or candidate.shape()=="number-images/15.gif":
                        initialBoard[i][j]=int(candidate.shape()[14:16])
                    else:
                        initialBoard[i][j]=int(candidate.shape()[14:15])
                j=j+1
        j=0
        i=i+1
    q=PriorityQueue()
    root = newNode(initialBoard, x, y, x, y, 0, None);
    root.cost = calculateCost(initialBoard, finalBoard);
    q.insert(root)
    matList.append(root)
    for i in range(4):
        if(isSafe(root.x + row[i], root.y + col[i])):
            child = newNode(root.mat, root.x,root.y, root.x + row[i],root.y + col[i],root.level + 1, root)
            if(child.mat not in matList):
                child.cost = calculateCost(child.mat, finalBoard)
                q.insert(child)
                root.child.append(child)
                matList.append(child.mat)
    min=root
    r=0
    count=0
    while not q.isEmpty():
        count=count+1
        if(count>20):
            return 0
        if(r!=0):
            t=getChild(min)
            while(t==None):
                t=getChild(min.parent)
                min=min.parent
            min=t
        r=r+1
        if(min.cost==0):
            printPath(min)
            return count
        for i in range(4):
            if(isSafe(min.x + row[i], min.y + col[i])):
                child = newNode(min.mat, min.x,min.y, min.x + row[i],min.y + col[i],min.level + 1, min)
                if(min.parent!=None and child.mat!=min.parent.mat or min.parent==None):
                    child.cost = calculateCost(child.mat, finalBoard)
                    q.insert(child)
                    min.child.append(child)


def new_window(i):
    playsound('button.wav')
    global counterWindow, window,canvas, counter2
    if(counterWindow==0):
        window = tk.Toplevel( )
        window.title("Solution")
        canvas = tk.Canvas(window, height=600, width=600)
        image = ImageTk.PhotoImage(file="bg.gif")
        canvas.create_image(0, 0, image=image, anchor=NW)
        canvas.pack()
        counterWindow=counterWindow+1
        counter2=1
    x=125
    y=110
    if(len(solutions)==0):
        messagebox.showinfo("Wohooo", "The solution has been reached")
        window.destroy()
        counterWindow=0

    img0 = PhotoImage(file=images[solutions[i][0]-1])
    canvas.create_image(x,y, anchor=NW, image=img0)       
    x=x+90
    img1 = PhotoImage(file=images[solutions[i][1]-1])
    canvas.create_image(x,y, anchor=NW, image=img1)       
    x=x+90
    img2 = PhotoImage(file=images[solutions[i][2]-1])
    canvas.create_image(x,y, anchor=NW, image=img2)       
    x=x+90
    img3 = PhotoImage(file=images[solutions[i][3]-1])
    canvas.create_image(x,y, anchor=NW, image=img3)       
    x=125
    y=y+90
    img4 = PhotoImage(file=images[solutions[i][4]-1])
    canvas.create_image(x,y, anchor=NW, image=img4)       
    x=x+90
    img5 = PhotoImage(file=images[solutions[i][5]-1])
    canvas.create_image(x,y, anchor=NW, image=img5)       
    x=x+90
    img6 = PhotoImage(file=images[solutions[i][6]-1])
    canvas.create_image(x,y, anchor=NW, image=img6)       
    x=x+90
    img7 = PhotoImage(file=images[solutions[i][7]-1])
    canvas.create_image(x,y, anchor=NW, image=img7)       
    x=125
    y=y+90
    img8 = PhotoImage(file=images[solutions[i][8]-1])
    canvas.create_image(x,y, anchor=NW, image=img8)       
    x=x+90
    img9 = PhotoImage(file=images[solutions[i][9]-1])
    canvas.create_image(x,y, anchor=NW, image=img9)       
    x=x+90        
    img10=PhotoImage(file=images[solutions[i][10]-1])
    canvas.create_image(x,y, anchor=NW, image=img10)
    x=x+90 
    img11=PhotoImage(file=images[solutions[i][11]-1])
    canvas.create_image(x,y, anchor=NW, image=img11)
    x=125
    y=y+90
    img12 = PhotoImage(file=images[solutions[i][12]-1])
    canvas.create_image(x,y, anchor=NW, image=img12)       
    x=x+90
    img13 = PhotoImage(file=images[solutions[i][13]-1])
    canvas.create_image(x,y, anchor=NW, image=img13)       
    x=x+90        
    img14=PhotoImage(file=images[solutions[i][14]-1])
    canvas.create_image(x,y, anchor=NW, image=img14)
    x=x+90 
    img15=PhotoImage(file=images[solutions[i][15]-1])
    canvas.create_image(x,y, anchor=NW, image=img15)

    buttonnew = tk.Button(canvas.master,text="Solve",fg="#5c9ca4",bd="30", padx="7", pady="7",
                              relief=RAISED,command=lambda: new_window(i))
    canvas.create_window(310, 50, window=buttonnew)
    #add img and display
    #after adding all img, we remove all the elements from solutions list

    #if solutions[i][j]==0, then take images[15], instead of images[solutions[i][j]]

    solutions.pop(0) #removing first element of list everytime

    mainloop()

def newFunc():
    playsound('button.wav')
    global start_time, steps, scramble, titlee
    titlee.clear()
    titlee.write("Steps : 0",align="center", font=("Times New Roman",20, "normal", 'bold'))
    x=scramble_board()
    print(x)
    while(x>20 or x<6):
       x=scramble_board()
    scramble=True
    counterWindow=0
    start_time = time.time() 
    steps=0


    
def create_scramble_button():
    # Uses a turtle with an image as a button.
    global screen
    canvas = screen.getcanvas()
    button1 = tk.Button(canvas.master,text="Scramble",fg="#5c9ca4",bd=5, padx="7", pady="7",
                              command=lambda: newFunc())
    canvas.create_window(10, -260, window=button1)

def find(p):
    # to find tile to swap
    global initialBoard, board, m , n
    for i in range(4):
        for j in range(4):
            if(board[i][j].shape()=="number-images/empty.gif" and p==0):
                m=i
                n=j
                return 
            if(board[i][j].shape()==f"number-images/{p}.gif"):
                m=i
                n=j
                return 


def reset():
    # to reset the game
    playsound('button.wav')
    global initialBoard, board, m ,n, steps, titlee

    for i in range(4):
        for j in range(4):
            x=board[i][j]
            find(initialBoard[i][j])
            board[i][j]=board[m][n]
            board[m][n]=x
    steps =0
    titlee.clear()
    titlee.write("Steps : %d"%steps,align="center", font=("Times New Roman",20, "normal", 'bold'))

    draw_board()


def create_reset_button():
    global window
    canvas = screen.getcanvas()
    button1 = tk.Button(canvas.master,text="Reset",  foreground="white",fg="#5c9ca4",bd=5, padx="7", pady="7",
                              command=lambda: reset())
    canvas.create_window(-80, -260, window=button1)


    
def create_solution_button():
    global window
    canvas = screen.getcanvas()
    button1 = tk.Button(canvas.master,text="Solution",  foreground="white",fg="#5c9ca4",bd=5, padx="7", pady="7",
                              command=lambda: new_window(0))
    canvas.create_window(100, -260, window=button1)


def main2():
    # screen3-winning screen
    global timee, screen, screen1, steps, sound, counterWindow, window, counter2
    sound=sound+1
    if(counter2==1):
        window.destroy()
        counterWindow=0
        counter2=0
    screen.clearscreen()
    screen1 = turtle.Screen()
    screen1.setup(600, 600)
    screen1.title("15 Puzzle")
    mainScreen1.bgpic("home1.gif")
    screen1.tracer(0)  # Disable animation
    print("{:.2f}".format(timee))
    titlee=turtle.Turtle()
    titlee.setpos(0,150)
    titlee.write("CONGRATULATIONS",align="center", font=("Times New Roman",55, "normal", 'bold', 'italic'))
    titlee=turtle.Turtle()
    titlee.setpos(0,90)
    titlee.write("You Win!",align="center", font=("Times New Roman",40, "normal", 'bold'))
    titlee=turtle.Turtle()
    titlee.setpos(0,30)
    titlee.write("Time taken: {:.2f} seconds".format(timee),align="center", font=("Times New Roman",20, "normal", 'bold'))
    titlee=turtle.Turtle()
    titlee.setpos(0,0)
    titlee.write("Steps taken: %d steps"%(steps),align="center", font=("Times New Roman",20, "normal", 'bold'))
    canvas = screen.getcanvas()
    button1 = tk.Button(canvas.master,text="Home Screen",fg="#5c9ca4",bd="30", padx="7", pady="7",
                              relief=RAISED,command=lambda: main())
    canvas.create_window(-90, 100, window=button1)
    button1 = tk.Button(canvas.master,text="Play Another Game",fg="#5c9ca4",bd="6", padx="7", pady="7",
                            relief=SUNKEN, command=lambda: main1(1,1))
    canvas.create_window(60, 100, window=button1)
    playsound('victory.wav')




def main1(x,y):
    # screen2-play screen
    global mainScreen1, start_time, steps, titlee, scramble, sound
    if(sound==0):
        playsound('go.wav')
    else:
        playsound('button.wav')
    mainScreen1.clearscreen()
    global screen, board , finalCount
    counterWindow=0
    steps=-1

    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("15 Puzzle")
    screen.bgpic("home1.gif")
    screen.tracer(0)  # Disable animation
    register_images()
    initialBoard = [[0 for c in range(4)] for r in range(4)]

    # Initialise game and display
    board = create_tiles()
    create_reset_button()
    create_solution_button()
    create_scramble_button()
    finalCount=finalCount+1
    x=scramble_board()
    print(x)
    while(x<6):
       x=scramble_board()
    scramble=True
    steps=steps+1
    titlee=turtle.Turtle()
    titlee.penup()
    titlee.hideturtle()
    titlee.setpos(0,200)
    titlee.write("Steps : 0",align="center", font=("Times New Roman",20, "normal", 'bold'))
    start_time = time.time() 
    print(solutions)
    screen.tracer(1)  # Restore animation
    counterWindow=0

hcount=0
images = []
solutions=[]
for i in range(NUM_ROWS * NUM_COLS - 1):
    file = f"number-images/{i+1}.gif" 
    images.append(file)

images.append("number-images/scramble.gif")
images.append("number-images/empty.gif")

def main():
    # screen1- home screen
    global mainScreen1, screen, hcount , steps, sound
    if(sound!=0):
        playsound('button.wav')
    sound=0
    if(hcount!=0):
        screen1.clearscreen()
    mainScreen1=turtle.Screen()
    mainScreen1.title("15 Puzzle")
    mainScreen1.bgpic("home1.gif")
    mainScreen1.setup(width=600, height=600)
    mainScreen1.tracer(0)

    titlee=turtle.Turtle()
    titlee.setpos(0,180)
    titlee.write("15 Puzzle",align="center", font=("Times New Roman",70, "normal", 'bold'))

    rules=turtle.Turtle()
    rules.goto(-140,100)
    rules.write("About the game:",align="center", font=("Times New Roman",40, "normal"))

    rule1=turtle.Turtle()
    rule1.goto(-275,70)
    rule1.write("A sliding puzzle having 15 tiles numbered 1–15 in a frame, leaving one unoccupied tile position.", align="left", font=("Times New Roman",13, "normal"))

    rule2=turtle.Turtle()
    rule2.goto(-275,40)
    rule2.write("Tiles in same row or column of the open position can be moved by sliding them horizontally or vertically.",align="left",  font=("Times New Roman",13, "normal"))

    rule3=turtle.Turtle()
    rule3.goto(-275,10)
    rule3.write("The goal of the puzzle is to place the tiles in numerical order.", align="left", font=("Times New Roman",13, "normal"))
    play=turtle.Turtle()
    play.goto(0,-120)
    play.write("Play Game?", align="center", font=("Times New Roman",45, "normal", "bold"))
    mainScreen1.onscreenclick(main1)

    hcount=hcount+1

sound=0
counter2=0
main()    
turtle.done()