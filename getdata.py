import numpy as np
import pygame
from pygame.locals import *
pygame.init()


def cmplx(v):
    return v[0] + v[1] * 1j


N = 10000
FPS = 360
W = 1000
center = (1 + 1j) * W / 2
disp = pygame.display.set_mode((W, W))
clock = pygame.time.Clock()

f = []

running = True
started = False
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN:
            started = True

        if e.type == MOUSEBUTTONUP:
            started = False

        if e.type == KEYDOWN and e.key == K_ESCAPE:
            running = False

        if e.type == MOUSEMOTION and started:
            pygame.draw.circle(disp, 0xff, e.pos, 3)
            f.append(cmplx(e.pos) - center)

    pygame.display.update()
    clock.tick(FPS)

arr = np.array(f, dtype=np.complex128)
np.savetxt("data.txt", arr)

pygame.quit()