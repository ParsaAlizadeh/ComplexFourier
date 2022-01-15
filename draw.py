import numpy as np
import pygame, sys, time
import matplotlib.pyplot as plt
from pygame.locals import *
pygame.init()


def vector(x, func=int):
    return (*map(func, (x.real, x.imag)),)


def getfrq():
    global N
    freq = np.arange(N)
    freq[freq >= N//2] = freq[freq >= N//2] - N
    return freq


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


def plot():
    plt.figure(figsize=(N//2, N//2))
    plt.title(f"N = {N}")
    plt.subplot(211)
    plt.bar(freq, np.abs(c))
    plt.xticks(freq)
    plt.grid()
    plt.subplot(212)
    plt.bar(freq, np.angle(c, deg=True))
    plt.xticks(freq)
    plt.grid()
    plt.show()


N = 50
dur = 20
W = 1000
center = (1 + 1j) * W / 2
disp = pygame.display.set_mode((W, W))
surf = pygame.surface.Surface((W, W))
clock = pygame.time.Clock()

freq = getfrq()
f = getdata("data.txt")
F = np.fft.fft(f, N)
c = F / N
ind = np.argsort(np.abs(c))[::-1]

for i in range(len(f)):
    pygame.draw.circle(surf, 0xff0000, vector(f[i] + center), 2)

# plot()

start = time.time()
running = True
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    timer = (time.time() - start) % dur

    disp.blit(surf, (0, 0))
    now = center
    pygame.draw.circle(disp, 0x0000ff, vector(now), 5)
    if abs(c[0]) != 0:
        last = now + c[0]
        pygame.draw.line(disp, 0x0000ff, vector(now), vector(last), 1)
        now = last
    for i in range(N):
        if ind[i] == 0 or abs(c[ind[i]]) == 0:
            continue
        last = now + c[ind[i]] * np.exp(2*np.pi*1j*freq[ind[i]]*timer/dur)
        pygame.draw.line(disp, 0xffffff, vector(now), vector(last), 2)
        now = last

    pygame.draw.circle(surf, 0x00ff00, vector(last), 2)

    pygame.display.update()

pygame.quit()
