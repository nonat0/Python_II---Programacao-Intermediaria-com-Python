import random
from typing import List, Tuple

def gerar_labirinto(width:int=31, height:int=31) -> Tuple[List[List[str]], Tuple[int,int]]:
    """
    Gera um labirinto usando recursive backtracker (DFS).
    Retorna a matriz do labirinto e a posição da maçã (row, col).
    """
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    lab = [['#' for _ in range(width)] for __ in range(height)]

    def carve(x, y):
        lab[y][x] = ' '
        dirs = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1 and lab[ny][nx] == '#':
                lab[y + dy//2][x + dx//2] = ' '
                carve(nx, ny)

    carve(1,1)

    path_cells = [(r,c) for r in range(1, height-1) for c in range(1, width-1) if lab[r][c] == ' ']
    apple_pos = random.choice(path_cells)
    lab[apple_pos[0]][apple_pos[1]] = '🍎'

    return lab, apple_pos
