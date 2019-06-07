import pygame
import os
from search import *
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state
from solution import *
from pygame.locals import *
from sys import exit

pygame.init()

# initialize screen
WIDTH = 720
HEIGHT = 720
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lockout")

# timer
FPS = 30
clock = pygame.time.Clock()
GRID_WIDTH = WIDTH // 20
Block = (WIDTH - 2 * GRID_WIDTH) // 5

background_img = pygame.image.load('images/back.png').convert()
rovers_images = ['rover1.png', 'rover2.png']
robots_images = ['robot1.png', 'robot2.png', 'robot3.png', 'robot4.png', 'robot5.png']
robots_load = [None for i in range(len(robots_images))]
rovers_load = [None for i in range(len(rovers_images))]
for i in range(len(robots_images)):
    robots_load[i] = pygame.image.load('images/' + robots_images[i]).convert()
for i in range(len(rovers_load)):
    rovers_load[i] = pygame.image.load('images/' + rovers_images[i]).convert()
# robot = pygame.image.load('images/robot.png').convert()
state = LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),))
all_chess = state.xanadus + state.robots

# 画出棋盘
def draw_background(surf):
    # 加载背景图片
    surf.blit(background_img, (0, 0))

    # 画网格线，棋盘为 19行 19列的
    # 1. 画出边框，这里
    rect_lines = [
        ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
        ((GRID_WIDTH, HEIGHT - GRID_WIDTH),
         (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((WIDTH - GRID_WIDTH, GRID_WIDTH),
         (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
    ]
    for line in rect_lines:
        pygame.draw.line(surf, BLACK, line[0], line[1], 2)

    # 画出中间的网格线
    for i in range(4):
        # 竖线
        pygame.draw.line(surf, BLACK,
                         (Block * (1 + i) + GRID_WIDTH, GRID_WIDTH),
                         (Block * (1 + i) + GRID_WIDTH, HEIGHT - GRID_WIDTH))

        # 横线
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH, Block * (1 + i) + GRID_WIDTH),
                         (HEIGHT - GRID_WIDTH, Block * (1 + i) + GRID_WIDTH))
    # change size
    # new_robot = pygame.transform.scale(robot, (Block, Block))
    # # show robot
    # screen.blit(new_robot, (Block + GRID_WIDTH, GRID_WIDTH))
    # # 画出棋盘中的五个点，围棋棋盘上为9个点，这里我们只画5个
    # circle_center = [
    #     (GRID_WIDTH * 4, GRID_WIDTH * 4),
    #     (WIDTH - GRID_WIDTH * 4, GRID_WIDTH * 4),
    #     (WIDTH - GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
    #     (GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
    #     (GRID_WIDTH * 10, GRID_WIDTH * 10)
    # ]
    # for cc in circle_center:
    #     pygame.draw.circle(surf, BLACK, cc, 5)


def draw_red_point(surf, mouse_x, mouse_y):
    pygame.draw.circle(surf, BLACK, (mouse_x, mouse_y), 30, 5)


def screen_position(pos: tuple):
    return (Block * pos[0] + GRID_WIDTH, Block * pos[1] + GRID_WIDTH)


def all_robots(state):
    """
    >>> state = LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),))
    >>> all_robots(state)
    ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4))
    """
    result = []
    robots = state.robots
    for robot_pos in robots:
        result.append(screen_position(robot_pos))
    return result


def all_rovers(state):
    result = []
    rovers = state.xanadus
    for rover_pos in rovers:
        result.append(screen_position(rover_pos))
    return result


def draw_all_robots(state):
    robots = all_robots(state)
    for i in range(len(robots)):
        # change size
        new_robot = pygame.transform.scale(robots_load[(i % 5)], (Block, Block))
        # show robot
        screen.blit(new_robot, (robots[i][0], robots[i][1]))


def draw_all_rovers(state):
    rovers = all_rovers(state)
    for i in range(len(rovers)):
        # change size
        new_rover = pygame.transform.scale(rovers_load[(i % 5)], (Block, Block))
        # show robot
        screen.blit(new_rover, (rovers[i][0], rovers[i][1]))


def click_chess(mouse_x, mouse_y):
    for item in all_chess:
        if GRID_WIDTH + Block * (item[0] + 1) > mouse_x > GRID_WIDTH + Block * item[0] and GRID_WIDTH + Block * (item[1] + 1) > mouse_y > GRID_WIDTH + Block * item[1]:
            draw_red_point(screen, mouse_x, mouse_y)

running = True
while running:
    # 设置屏幕刷新频率
    clock.tick(FPS)

    # 处理不同事件
    for event in pygame.event.get():
        # 检查是否关闭窗口
        if event.type == pygame.QUIT:
            running = False

    # 画出棋盘
    draw_background(screen)
    draw_all_robots(state)
    draw_all_rovers(state)
    # draw_red_point(screen)
    # 刷新屏幕
    pygame.display.flip()

    mouse_x, mouse_y = 0, 0
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click_chess(mouse_x, mouse_y)
                # screen.fill((mouse_x, mouse_y, 0))
                # screen.blit(text, (40, 100))
                pygame.display.update()
