import pygame
import time
import random
import heapq
import numpy as np

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements)==0

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority,item))

    def get(self):
        return heapq.heappop(self.elements)

class GridwithWeights():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.weights = {}

    def in_bounds(self,id):
        x,y = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self,id):
        return id not in self.walls

    def neighbors(self, id):
        x,y =id
        neighbors = [(x+20, y), (x-20, y), (x, y-20), (x, y+20)] # E W N S
        if (x + y) % 2 == 0:
            neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        x1,y1 = from_node
        x2,y2 = to_node
        return np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

pygame.init()

white = (255, 255, 255)
black = (0,0,0)
red = (255, 0, 0)
blue = (0,0,255)
yellow = (255, 255, 102)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_width))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_speed = 10
snake_block = 20

font_style = pygame.font.SysFont(None, 30)

def heuristic(a,b):
    x1,y1 = a
    x2,y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue() # open set
    frontier.push(start,0)
    came_from = {} # close set
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    path = []

    while not frontier.empty():
        curr_prior, current  = frontier.get()
        print(curr_prior)
        path.append(current)
        if current == goal:
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priorty = new_cost +heuristic(goal, next)
                frontier.push(next, priorty)
                came_from[next] = current
    return path, came_from, cost_so_far

def show_snake(snake_block, snake_list):
    for idx,x in enumerate(snake_list):
        if idx == len(snake_list)-1:
            # draw head
            pygame.draw.rect(dis, yellow, [x[0], x[1], snake_block, snake_block])
        else:
            pygame.draw.rect(dis, black, [x[0],x[1], snake_block, snake_block])

def show_score(score):
    value = font_style.render("Score: "+str(score), True, yellow)
    dis.blit(value,[0,0])

def message(msg, color):
    messg = font_style.render(msg, True, color)
    dis.blit(messg, [dis_width/6, dis_height/3])

def auto_game():
    game_over = False
    game_end = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    snake_list = []
    len_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    graph = GridwithWeights(dis_width, dis_height)

    while not game_over:
        while game_end == True:
            dis.fill(blue)
            message("You lost! Press Q-Quit or C-Play Again", red)
            show_score(len_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_c:
                        auto_game()

        path, came_from, cost = a_star_search(graph, (x1,y1), (foodx, foody))
        for (i,j) in path:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_end = True

            x1 = i
            y1 = j
            dis.fill(blue)
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > len_snake:
                del snake_list[0]

            # for x in snake_list[:-1]:
            #     if x == snake_head:
            #         game_end = True

            show_snake(snake_block, snake_list)
            show_score(len_snake - 1)
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                len_snake += 1
            clock.tick(snake_speed)

    pygame.quit()
    quit()


def game_loop():
    game_over = False
    game_end = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    len_snake = 1

    foodx = round(random.randrange(0, dis_width-snake_block)/snake_block)*snake_block
    foody = round(random.randrange(0, dis_height-snake_block)/snake_block)*snake_block

    while not game_over:
        while game_end==True:
            dis.fill(blue)
            message("You lost! Press Q-Quit or C-Play Again", red)
            show_score(len_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type==pygame.KEYDOWN:
                    if event.key ==pygame.K_q:
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_end = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1,y1]
        snake_list.append(snake_head)
        if len(snake_list)>len_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x==snake_head:
                game_end = True

        show_snake(snake_block, snake_list)
        show_score(len_snake-1)
        pygame.display.update()

        if x1==foodx and y1==foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            len_snake += 1
        clock.tick(snake_speed)

    pygame.quit()
    quit()

auto_game()


