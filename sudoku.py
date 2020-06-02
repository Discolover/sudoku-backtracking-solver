# au BufWritePost sudoku.py !time python sudoku.py
############################################################

def parse_sudoku(sudoku_file):
    sudoku = [['']*9 for _ in range(9)]
    f = open(sudoku_file)
    nonblank_line_cnt = 0
    for line in f:
        if nonblank_line_cnt >= 9: break
        if line.isspace(): continue
        nonblank_sym_cnt = 0
        for sym in line:
            if nonblank_sym_cnt >= 9: break
            if sym.isspace(): continue
            if sym.isdigit() and sym != '0':
                sudoku[nonblank_line_cnt][nonblank_sym_cnt] = sym
            nonblank_sym_cnt += 1
        nonblank_line_cnt += 1
    f.close()
    return sudoku

def print_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            print(sudoku[i][j] if sudoku[i][j] != '' else '-', end = '')
            if (j+1) % 3 == 0: print(end = ' ')
        print()
        if (i+1) % 3 == 0: print()
    
############################################################

def init_possible(sudoku):
    possible = [[init_cell_possible(sudoku, y, x) if sudoku[y][x] == '' else [] \
        for x in range(9)] for y in range(9)]
    return possible

def init_cell_possible(sudoku, y, x):
    cell_possible = [str(i) for i in range(1, 10)]
    scan_box(sudoku, cell_possible, y, x)
    scan_cross(sudoku, cell_possible, y, x)
    return cell_possible

def scan_box(sudoku, cell_possible, y, x):
    iy = y - y % 3
    ix = x - x % 3
    for row in range(iy, iy + 3):
        for col in range(ix, ix + 3):
            if sudoku[row][col] and sudoku[row][col] in cell_possible:
                cell_possible.remove(sudoku[row][col])
                
def scan_cross(sudoku, cell_possible, y, x):
    for row in range(9):
        if int(row / 3) == int(y / 3): continue
        if sudoku[row][x] and sudoku[row][x] in cell_possible:
            cell_possible.remove(sudoku[row][x])
    for col in range(9):
        if int(col / 3) == int(x / 3): continue
        if sudoku[y][col] and sudoku[y][col] in cell_possible:
            cell_possible.remove(sudoku[y][col])

############################################################

def bt(sudoku, possible, empty_cell_cnt):
    if empty_cell_cnt == 0:
        print_sudoku(sudoku)
        return True

    y, x = next_empty(sudoku, possible)

    if y < 0 and x < 0: return

    cur_possible = possible[y][x]
    possible[y][x] = []
    
    for val in cur_possible:
        sudoku[y][x] = val
        tied = get_tied(sudoku, possible, y, x)
        for r, c in tied:
            possible[r][c].remove(val)
        if bt(sudoku, possible, empty_cell_cnt - 1):
            return True
        for r, c in tied:
            possible[r][c].append(val)
            
    sudoku[y][x] = ''
    possible[y][x] = cur_possible

def next_empty(sudoku, possible):
    minn = 10
    next_empty_cell = (-1, -1)
    for y in range(9):
        for x in range(9):
            cell_possible = possible[y][x]
            if sudoku[y][x]: continue
            if len(cell_possible) < minn: 
                next_empty_cell = (y, x)
                minn = len(cell_possible)
    return next_empty_cell

def get_tied(sudoku, possible, y, x):
    return box(sudoku, possible, sudoku[y][x], y, x) \
        + cross(sudoku, possible, sudoku[y][x], y, x)

def box(sudoku, possible, val, y, x):
    iy = y - y % 3
    ix = x - x % 3
    tied = []
    for row in range(iy, iy + 3):
        for col in range(ix, ix + 3):
            if not sudoku[row][col] and (val in possible[row][col]):
                tied.append((row, col))
    return tied
                
def cross(sudoku, possible, val, y, x):
    tied = []
    for row in range(9):
        if int(row / 3) == int(y / 3): continue
        if not sudoku[row][x] and (val in possible[row][x]):
            tied.append((row, x))
    for col in range(9):
        if int(col / 3) == int(x / 3): continue
        if not sudoku[y][col] and (val in possible[y][col]):
            tied.append((y, col))
    return tied

############################################################
def solve(values):
    pssbl = init_possible(values)
    empty_cell_cnt = sum(1 if cell == '' else 0 for row in values for cell in row)
    return bt(values, pssbl, empty_cell_cnt)


if __name__ == '__main__':
    sudoku = parse_sudoku('sample')
    print_sudoku(sudoku)
    pssbl = init_possible(sudoku)
    empty_cell_cnt = sum(1 if cell == '' else 0 for row in sudoku for cell in row)
    bt(sudoku, pssbl, empty_cell_cnt)

    # while s := input():
    #     row, col = [int(num) for num in s.split()]
    #     print(get_tied(sudoku, pssbl, row, col))
    #     print('-'*10)
    
