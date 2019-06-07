import pygame
import os
from search import *
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state
from solution import *

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


background_img = pygame.image.load('images/back.png').convert()


# 画出棋盘
def draw_background(surf):
    # 加载背景图片
    surf.blit(background_img, (0, 0))

    # 画网格线，棋盘为 19行 19列的
    # 1. 画出边框，这里
    GRID_WIDTH = WIDTH // 20
    Block = (WIDTH - 2 * GRID_WIDTH) // 5
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
        pygame.draw.line(surf, BLACK,
                         (Block * (1 + i) + GRID_WIDTH, GRID_WIDTH),
                         (Block * (1 + i) + GRID_WIDTH, HEIGHT - GRID_WIDTH))

        # 横线
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH, Block * (1 + i) + GRID_WIDTH),
                         (HEIGHT - GRID_WIDTH, Block * (1 + i) + GRID_WIDTH))

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

    # 刷新屏幕
    pygame.display.flip()