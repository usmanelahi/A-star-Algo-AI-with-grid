
import pygame
import math
import heapq
import random
from collections import defaultdict
pygame.init()
WIDTH = 720 
ROWS=40
WIN = pygame.display.set_mode((WIDTH, WIDTH))
RED = (255,0,0)
GREEN = (0,255, 0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
TURQUOISE = (64,224,208)
BLUE=(0,0,255)
BOX=(128,128,128)
graph=defaultdict(list)
size=WIDTH//ROWS
class Block:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.x=row*size
        self.y=col*size
        self.color=WHITE
        self.g=float("inf")
        self.h=float("inf")
        self.f=float("inf")
        self.parent=None       
    def __lt__(self,other):
         return self.f<other.f

def draw(grid):
    WIN.fill(WHITE)
    for row in grid:
        for block in row:
            pygame.draw.rect(WIN,block.color,(block.x,block.y,size,size))
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * size), (WIDTH, i * size))
    for j in range(ROWS):
        pygame.draw.line(WIN, BLACK, (j * size, 0), (j * size, WIDTH))

def AstarAlgo(start,end,grid,barrier):
    openList=[]
    heapq.heapify(openList)
    start.h=0
    start.g=0
    start.f=abs(start.x-end.x) + abs(start.y-end.y) 
    end.g=0
    end.f=0
    end.h=0
    closeList=[]
    heapq.heappush(openList,start)
    while len(openList)>=1:
        current=heapq.heappop(openList)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if current.color !=YELLOW and current.color !=TURQUOISE:
            current.color=BLUE
            closeList.append(current)
        if current.x == end.x and current.y == end.y:
            while True:
                current=current.parent
                if current.color ==YELLOW:
                    break
                if current.color !=RED and current.color != BLACK:
                    current.color=BOX
            draw(grid)
            pygame.display.update()
            return True
        for neighbour in graph[current]:
            if neighbour in closeList:
                continue
            if neighbour in barrier:
                continue
            if neighbour.color == RED:
                neighbour.g=current.g+100
            else:
                neighbour.g=current.g+1
            neighbour.h=abs(neighbour.x-end.x) + abs(neighbour.y-end.y) 
            neighbour.f=neighbour.g+neighbour.h
            if neighbour.color !=YELLOW and neighbour.color !=TURQUOISE and neighbour.color !=RED:
                neighbour.color=GREEN
            neighbour.parent=current
            heapq.heappush(openList,neighbour)
            heapq.heapify(openList)
        draw(grid)
        pygame.display.update()
    return False

def markGraph():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            block = Block(i, j)
            grid[i].append(block)
    for row in grid:
        for node in row:
            graph[node]=[]
            if node.row <ROWS-1:
                graph[node].append(grid[node.row+1][node.col])
            if node.row >0:
                graph[node].append(grid[node.row-1][node.col])
            if node.col < ROWS-1:
                graph[node].append(grid[node.row][node.col + 1])
            if node.col > 0:
                graph[node].append(grid[node.row][node.col - 1])
    return grid

def instructions():
    WIN.fill(WHITE)
    font1=pygame.font.SysFont(pygame.font.get_default_font(),40)
    img=font1.render("INSTRUCTIONS",True,BLUE)
    WIN.blit(img,(3*size,3*size))
    img4=font1.render("RED = TRAFFIC JAM -- 1'st click Set Automatically",True,BLUE)
    WIN.blit(img4,(3*size,7*size))
    img1=font1.render("YELLOW = START POSITION -- 2'nd Right click",True,BLUE)
    WIN.blit(img1,(3*size,10*size))
    img2=font1.render("LIGHT BLUE = END -- 3'rd Right Click",True,BLUE)
    WIN.blit(img2,(3*size,13*size))
    img3=font1.render("BLACK = ROAD BLOCKS -- 4'th Right Click",True,BLUE)
    WIN.blit(img3,(3*size,16*size))
    img5=font1.render("Press space bar to start search for Path",True,BLUE)
    WIN.blit(img5,(3*size,19*size))
    img6=font1.render("PRESS ANY KEY TO CONTINUE",True,RED)
    WIN.blit(img6,(3*size,26*size))
    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                run=False
                break

def main():
    instructions()
    grid=markGraph()
    start = None
    end = None
    traffic=False
    run= True
    barrier=[]
    while run:
        draw(grid)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row=(pos[0]//(WIDTH//ROWS))
                col =(pos[1]//(WIDTH//ROWS))
                block = grid[row][col]
                if traffic == False:
                    for i in range(int(ROWS * 0.4)):
                        r=random.randint(1,(WIDTH//ROWS)-1)
                        c=random.randint(1,(WIDTH//ROWS) -1)
                        node=grid[r][c]
                        node.color=RED
                    traffic=True
                elif not start and block != end and block.color !=RED:
                    start = block
                    start.color=YELLOW
                elif not end and block != start and block.color != RED:
                    end = block
                    end.color=TURQUOISE
                elif block != end and block != start:
                    block.color=BLACK
                    barrier.append(block)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    val=AstarAlgo(start,end,grid,barrier)
                    if val ==True:
                        run =False
    pygame.time.delay(5*1000)
    pygame.quit()

main()
