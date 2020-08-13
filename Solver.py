# This project solves sudoku puzzles using a depth-first, brute-force algorithm

from time import sleep
import tkinter as tk
from tkinter import filedialog, StringVar, Entry

""" functions """

""" callback for text objects (event listener) """
def callback(sv, x,y):
    string = sv.get()
    valid = True
    
    if not '\n' in sv.get():  
        if len(string) > 1:
            string = string[-1:]
            sv.set(string)
        if not string[-1:].isnumeric():
            valid = False
        elif int(string) == 0:
            string = ''
            sv.set('')
    else:
        sv.set(sv.get().replace('\n', ''))
        valid = False
    
    if valid:
        entries[x][y].config(fg = "black")
    else:
        entries[x][y].config(fg = "red")
        
    return True

""" method for opening sudoku puzzle """
def openPuzzle():
    # lock other buttons
    solvePuzzle["state"] = "disabled"
    resetButton["state"] = "disabled"
    
    fileName = filedialog.askopenfilename(initialdir="/", title = "Select Puzzle",
                                          filetypes = (('Text Files', '.txt'), ('All Files', '*.*')))

    counter = 0
    file = open(fileName, "r")
    while(True):
        # get next line
        line = file.readline().split()
        
        # if its null, end loop
        if not line:
            break
        
        # save line
        for n in range(9):
            numbers[n][counter].set(line[n])
            
        counter += 1
        
    for x in range(9):
        for y in range(9):
            if len(numbers[y][x].get()) > 1:
                numbers[y][x].set(numbers[y][x].get() + '\n')
            if not numbers[y][x].get().isnumeric():
                numbers[y][x].set(numbers[y][x].get() + '\n')
            elif numbers[y][x].get() == '0':
                numbers[y][x].set(' ')
                
    # unlock other buttons
    solvePuzzle["state"] = "normal"
    resetButton["state"] = "normal"

""" a reset button that empties all numbers """
def reset():
    for rows in numbers:
        for num in rows:
            num.set('')
            
def updateGrid():
    sleep(.03)
    
""" method to validate puzzle before solving """
def validate():
    # lock all buttons
    openFile["state"] = "disabled"
    solvePuzzle["state"] = "disabled"
    resetButton["state"] = "disabled"
    
    # rows(x,y) x=row, y=1-9
    rows = [[None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None]]
    
    #each row represents a section
    sections = [[None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None],
              [None,None,None,None,None,None,None,None,None]]
    
    solvable = True
    
    for x in range(9):
        columns = [None,None,None,None,None,None,None,None,None]
        for y in range(9):
            if numbers[x][y].get() != '':
                valid = True
                number = int(numbers[x][y].get())
                
                # check if it is a number or length is > 1
                if not numbers[x][y].get().isnumeric or len(numbers[x][y].get()) > 1:
                    solvable = False
                elif number != 0:
                    # check rows for duplicates
                    if rows[y][number-1] is not None: # we want to lock the y height so we can iterate through the row
                        entries[x][y].config(fg = "red")
                        rows[y][number-1].config(fg = "red")
                        valid = False
                        solvable = False
                    else:
                        rows[y][number-1] = entries[x][y]
                        
                    # check columns for duplicates
                    if columns[number-1] is not None:
                        entries[x][y].config(fg = "green")
                        columns[number-1].config(fg = "green")
                        valid = False
                        solvable = False
                    else:
                        columns[number-1] = entries[x][y]
                        
                    # check sections for duplicates
                    sectionNumber = (x // 3) + (y // 3)*3
                    if sections[sectionNumber][number-1] is not None:
                        entries[x][y].config(fg = "blue")
                        sections[sectionNumber][number-1].config(fg = "blue")
                        valid = False
                        solvable = False
                    else:
                        sections[sectionNumber][number-1] = entries[x][y]
                    
                    # turn font to black if its valid
                    if valid:
                        entries[x][y].config(fg = "black")
    
    # if solvable, solve it
    if solvable:
        solve()
        
    # lock all buttons
    openFile["state"] = "normal"
    solvePuzzle["state"] = "normal"
    resetButton["state"] = "normal"
            
""" recursive algorithm that solves sudoku """
def solve():
    # check every spot for empty spots
    for x in range(9):
        for y in range(9):            
            # find a blank spot
            if numbers[x][y].get() == '':
                # find all the numbers it could be
                possibleAnswers = possible(x, y)
                
                # try each answer
                for ans in possibleAnswers:
                    numbers[x][y].set(ans)
                    entries[x][y].config(fg="blue")
                    root.update()
                    found = solve()
                    
                    # if recursion solved it, stop loop
                    if found:
                        return True
                    
                    # otherwise undo the changes and continue
                    numbers[x][y].set('')
                    entries[x][y].config(fg="black")
                # if no answer worked, return to previous recursion
                return False
    #solution found
    return True
    
""" method that determines which numbers are possible solutions for 1 space """
def possible(x, y):
    possible = [1,2,3,4,5,6,7,8,9]
    
    # check section offset for the square
    sectionX = (x // 3) * 3
    sectionY = (y // 3) * 3
    
    # check for possible numbers
    for i in range(9):
        # check columns
        current = numbers[i][y].get()
        if current != '':
            if int(current) in possible:   
                possible.remove(int(current))
        # check rows
        current = numbers[x][i].get()
        if current != '':
            if int(current) in possible:    
                possible.remove(int(current))
        # check section
        current = numbers[sectionX + (i//3)][sectionY + (i%3)].get()
        if current != '':
            if int(current) in possible:
                possible.remove(int(current))
    
    return possible

""" Main """
# puzzle for reset button
resetPuzzle = []

# Create gui
root = tk.Tk()
root.title("Sudoku Solver")
root.resizable(False, False)

canvas = tk.Canvas(root, height = 500, width = 500, bg="#A5A5A5")
canvas.create_rectangle(20,20, 480,480, fill = "white", width = 5)
canvas.pack()

#puzzle outline
#columns
canvas.create_line(71,20, 71,480, width = 1)
canvas.create_line(122,20, 122,480, width = 1)
canvas.create_line(173,20, 173,480, width = 4)
canvas.create_line(224,20, 224,480, width = 1)
canvas.create_line(275,20, 275,480, width = 1)
canvas.create_line(328,20, 328,480, width = 4)
canvas.create_line(379,20, 379,480, width = 1)
canvas.create_line(430,20, 430,480, width = 1)

#rows
canvas.create_line(20,71, 480,71, width = 1)
canvas.create_line(20,122, 480,122, width = 1)
canvas.create_line(20,173, 480,173, width = 4)
canvas.create_line(20,224, 480,224, width = 1)
canvas.create_line(20,275, 480,275, width = 1)
canvas.create_line(20,328, 480,328, width = 4)
canvas.create_line(20,379, 480,379, width = 1)
canvas.create_line(20,430, 480,430, width = 1)

#number texts
font = {'font': (None, 20)}
entries = []
numbers = []
for x in range(9):
    # make numbers and entries 2d lists
    row1 = []
    row2 = [] # strange things were happening when trying to use only 1 'row[]'
    numbers.append(row1)
    entries.append(row2)
    for y in range(9):
        # get string var
        sv = StringVar()
        sv.set('')
        sv.trace("w", lambda *_, var = sv, x=x, y=y: callback(var,x,y))
        numbers[x].append(sv)
        
        # get entry and attach string var
        num = Entry( canvas, textvariable = sv, width = 2, **font)
        num.grid(column = x, row = y, padx = (8), pady = (7))
        entries[x].append(num)
        
        #offset grid
        if x == 0:
            num.grid(padx = (34,8))
        if x == 8:
            num.grid(padx = (8, 34))
        if y == 0:
            num.grid(pady = (33,7))
        if y == 8:
            num.grid(pady = (7, 33))

# button for opening a puzzle
openFile = tk.Button(root, text = "Open File", padx = 10, pady = 10, fg="Black", command = openPuzzle)
openFile.pack()

# button for solving puzzle
solvePuzzle = tk.Button(root, text = "Solve", padx = 10, pady = 10, fg="Black", command = validate)
solvePuzzle.pack()

# button to reset
resetButton = tk.Button(root, text = "Reset", padx = 10, pady = 10, fg="Black", command = reset)
resetButton.pack()

root.mainloop()
