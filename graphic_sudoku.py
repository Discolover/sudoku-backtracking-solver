# Think about why on_* type methods are unlogical here.
# Solve x,y and y,x ordering issue
from tkinter import Canvas
from tkinter.font import Font
import tkinter
import sudoku

CELL_COLOR = "#FFFDFD"
OBSCURE_CELL_COLOR = "#CBD2D0"
DIGIT_COLOR = "#0B3CF9"
SOLVED_DIGIT_COLOR = "#731963"


class Sudoku(Canvas):
    def __init__(self, size, values):
        Canvas.__init__(self)
        self.config(width = size, height = size)
        self.size = size
        sudoku.font = Font(size = int(32 * self.size / 600))
        self.values = values
        self.curyx = (4, 4)
        sudoku.INDEXES = [(x, y) for x in range(9) for y in range(9)]
        self.pack()
        self.init_graphics()
        self.event_add('<<digit>>', *['<KeyPress-{}>'.format(i) for i in range(1, 10)])
        self.bind_all('<<digit>>', self.write_digit)
        self.bind_all('s', self.solve)
        self.bind_all('c', self.clear)
        self.bind('<Motion>', self.on_mouse_motion)
        self.bind('<Button-1>', self.on_mouse_click1)
        self.bind('<Button-3>', self.on_mouse_click3)
        
    def init_graphics(self):
        # draw and initialize cells
        self.cells = {}
        sz = self.size / 9
        for x, y in sudoku.INDEXES:
            self.cells[(y, x)] = self.create_rectangle(x * sz, y * sz, x * sz + sz, y * sz + sz \
                , fill = CELL_COLOR)
        # draw and initialize digits
        self.digits = {}
        for x, y in sudoku.INDEXES:
            self.digits[(y, x)] = self.create_text(x * sz + sz / 2, y * sz + sz / 2 \
                , font = sudoku.font, text = self.values[y][x], fill = DIGIT_COLOR)
        # draw boxes
        for x in range(1, 3):
            self.create_line(x * self.size / 3, 0, x * self.size / 3, self.size, width = 3)
        for y in range(1, 3):
            self.create_line(0, y * self.size / 3, self.size, y * self.size / 3, width = 3)

    def draw_digits(self): 
        for x, y in sudoku.INDEXES:
            digit = self.digits[(y, x)]
            color = DIGIT_COLOR if self.itemcget(digit, 'text') != '' else SOLVED_DIGIT_COLOR
            self.itemconfig(
                digit,
                fill = color,
                text = self.values[y][x]
            )

    def on_mouse_motion(self, event):
        y, x  = int(event.y / (self.size/9)) , int(event.x / (self.size/9))
        if x >= 9: x = 8
        if y >= 9: y = 8
        newyx = (y, x)
        if self.curyx != newyx:
            self.itemconfig(self.cells[newyx], fill = OBSCURE_CELL_COLOR)
            self.itemconfig(self.cells[self.curyx], fill = CELL_COLOR)
            self.curyx = newyx
    
    def on_mouse_click1(self, event):
        self.master.destroy()

    def on_mouse_click3(self, event):
        self.itemconfig(self.digits[self.curyx], text = '')

    def write_digit(self, event):
        self.itemconfig(self.digits[self.curyx], text = event.char, fill = DIGIT_COLOR)
        y, x = self.curyx
        self.values[y][x] = event.char

    def solve(self, event):
        sudoku.print_sudoku(self.values)
        if sudoku.solve(self.values):
            self.draw_digits()
    
    def clear(self, event):
        for y, x in sudoku.INDEXES:
            self.values[y][x] = ''
        self.draw_digits()
            
    

s = Sudoku(600, sudoku.parse_sudoku('sample'))
tkinter.mainloop()
