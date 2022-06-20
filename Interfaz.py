import Agent

import pygame as pg
import sys, os
pg.init()
background_colour = (125,125,125)
(width, height) = (1280, 720)
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Agents')
x=20
myfont = pg.font.SysFont("JetBrainsMono NF", 40)
text = myfont.render(str(x), True, (255,255,0), (0,255,255))
textRect = text.get_rect()
textRect.center = (100, 100)
pg.display.flip()
reloj = pg.time.Clock()
running = True

def mapa():
    screen.fill(background_colour)
    for i in range(24):
        pg.draw.rect(screen, (255,255,255), pg.Rect(0, 20+i*30, 1280, 4))   
    for i in range(43):
        pg.draw.rect(screen, (255,255,255), pg.Rect(20+i*30, 0, 4, 720))


text = open('Agente.txt')
T=[]
OC=[]
DT=[]
DA=[]
OS=[]
DM=[]
PH=[]
RE=[]
for line in text.read().splitlines():
    if line.startswith("T:"):
        _, t=line.split(":")
        T.append([t])
    if line.startswith("OC:"):
        _,oc=line.split("OC:")
        a,b,c=oc.split(",")
        q=[a,b,c]
        OC.append(q)
    if line.startswith("DT:"):
        _,dt=line.split("DT:")
        a,b=dt.split(",")
        q=[a,b]
        DT.append(q)
    if line.startswith("DA:"):
        _,da=line.split("DA:")
        a,b=da.split(",")
        q=[a,b]
        DA.append(q)
    if line.startswith("OS:"):
        _,os=line.split("OS:")
        a,b=os.split(",")
        q=[a,b]
        OS.append(q)
    if line.startswith("DM:"):
        _,dm=line.split("DM:")
        DM.append([dm])
    if line.startswith("PH:"):
        _,ph=line.split("PH:")
        PH.append([ph])
    if line.startswith("RE:"):
        _,re=line.split("RE:")
        RE.append([re])


posx=22
posy=22
pg.draw.circle(screen,(0,255,0) , (posx,posy), 2)
R = pg.draw.rect(screen, (255,0,0), pg.Rect(30, 15, 10, 10),2)
pg.display.update()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                mapa()
                posx = posx - 10
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                pg.draw.circle(screen, (255,255,255), (posx, posy), 2)
                pg.display.update(posx-2,posy-2,4,4)
                #mapa()
                posx = posx + 10
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mapa()
                posy = posy - 10
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                mapa()
                posy = posy + 10
        if event.type == pg.MOUSEMOTION:
            if R.collidepoint(pg.mouse.get_pos()):
                screen.blit(text,textRect)
                x,y = pg.mouse.get_pos()
                print(x,y)
            #else:
                #Posiciones
                # mapa()
                # pg.display.flip()
                
    pg.draw.circle(screen, (0,255,0), (posx, posy), 2)
    pg.display.update(posx-2,posy-2,4,4)
    pg.display.flip()
    
pg.quit()