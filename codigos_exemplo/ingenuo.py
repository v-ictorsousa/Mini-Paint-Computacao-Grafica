import sys,pygame
from pygame import gfxdraw

pygame.init()
screen = pygame.display.set_mode((400,400))
screen.fill((0,0,0))
pygame.display.flip()

white=(255,255,255)

#Esta funcao funciona apenas
#para o primeiro quadrante
def bezierIngenuo(p1,p2,p3,p4):
    for t in xrange(0,1,0.01):
        omt  = 1-t
        omt2 = omt*omt
        omt3 = omt2*omt
        t2   = t*t
        t3   = t2*t
        x    = omt3 * p1[0] + ((3*omt2)*t*p1[0]) +     (3*omt*t2*p3[0])+t3*p4[0]
        y    = omt3 * p1[1] + ((3*omt2)*t*p1[1]) + (3*omt*t2*p3[1])+t3*p4[1]


        x = round(x, 0)
        y = round(y, 0)

        screen.set_at((x, y), white)
        pygame.display.flip()

bezierIngenuo(10, 10, 50, 50)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
