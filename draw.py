import numpy as np
import pygame, sys, time
from pygame.locals import *
pygame.init()


def vector(x, func=int):
    return (*map(func, (x.real, x.imag)),)


def getfrq(x):
    global N
    if x < N//2:
        return x
    return x - N


def getdata(fname):
    global N
    f = np.loadtxt(fname, np.complex128)
    arr = np.zeros(N, dtype=np.complex128)
    cnt = np.zeros(N)
    ind = np.linspace(0, len(f) - 1, N, dtype=np.int32)
    for i in range(N):
        arr[i] += f[ind[i]]
        cnt[i] += 1
    cnt[cnt == 0] = 1
    arr /= cnt
    return arr


N = 5
dur = 10
W = 500
center = (1 + 1j) * W / 2
disp = pygame.display.set_mode((W, W))
surf = pygame.surface.Surface((W, W))
clock = pygame.time.Clock()

f = getdata("data.txt")
F = np.fft.fft(f, N)
c = F / N
ind = np.argsort(abs(c))[::-1]

start = time.clock()
running = True
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    timer = (time.clock() - start) % dur

    disp.blit(surf, (0, 0))
    now = center
    for i in range(N):
        if abs(c[ind[i]]) == 0:
            continue
        last = now + c[ind[i]] * np.exp(2*np.pi*1j*getfrq(ind[i])*timer/dur)
        pygame.draw.line(disp, 0xffffff, vector(now), vector(last), 2)
        now = last

    pygame.draw.circle(surf, 0xff00, vector(last), 2)

    pygame.display.update()

pygame.quit()
