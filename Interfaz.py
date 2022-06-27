from agent import *

import pygame as pg
import sched, time
import sys, os

pg.init()
background_colour = (125,125,125)
(width, height) = (1285, 720)
# (width, height) = (1290, 730)
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Agents')
x=20
myfont = pg.font.SysFont("JetBrainsMono NF", 20)


# text = myfont.render(str(x), True, (255,255,0), (0,255,255))
# textRect = text.get_rect()

# textRect.center = (100, 100)
pg.display.flip()
reloj = pg.time.Clock()
running = True


speed = 0.001

# def mapa():
#     screen.fill(background_colour)
#     for i in range(24):
#         pg.draw.rect(screen, (255,255,255), pg.Rect(0, 20+i*30, 1280, 4))   
#     for i in range(43):
#         pg.draw.rect(screen, (255,255,255), pg.Rect(20+i*30, 0, 4, 720))

# def people(app:SimulatedApp):
#     for person in app.people:
#         posx, posy = person.position
#         pg.draw.circle(screen, (0,0,255), (posx, posy), 2)


selected_restaurant = None
#print(selected_restaurant)

def show_restaurant_orders():
    restaurant =selected_restaurant
    posx, posy = restaurant.position
    x= (len(restaurant.currentOrders), len(restaurant.doneOrders))
    text = myfont.render(str(x), True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (posx-20, posy)
    screen.blit(text,textRect)


def init_draw(app:SimulatedApp):
    # global text
    # global textRect
    # draw static things, the map for example
    screen.fill(background_colour)
    for i in range(24):
        pg.draw.rect(screen, (255,255,255), pg.Rect(0, 20+i*30, 1280, 4))   
    for i in range(43):
        pg.draw.rect(screen, (255,255,255), pg.Rect(20+i*30, 0, 4, 720))    
    # people
    for person in app.people:
        posx, posy = person.position
        # pg.draw.circle(screen, (0,0,255), (posx, posy), 2)
        person.circle = pg.draw.circle(screen, (255,255,0), (posx, posy), 2)
        if person.hasOrdered:
            posx, posy = person.address
            # pg.draw.circle(screen, (255,255,0), (posx, posy), 2)
            pg.draw.circle(screen, (0,0,255), (posx, posy), 2)
    # restaurants
    for restaurant in app.restaurants:
        posx, posy = restaurant.position
        if len(restaurant.currentOrders) >= restaurant.capacity:
            restaurant.rect = pg.draw.rect(screen, (255,0,0), pg.Rect(posx, posy, 10, 10), 2)
        else:
            restaurant.rect = pg.draw.rect(screen, (0,255,0), pg.Rect(posx, posy, 10, 10), 2)
        posx, posy = person.address
        pg.draw.circle(screen, (255,255,0), (posx, posy), 2)

        # print("current:", [restaurant.currentOrders)
        #print("done", [ e.id for e in restaurant.doneOrders ])
        
        #show_restaurant_orders()
        # pg.draw.circle(screen, (0,0,255), (posx, posy), 2)


selected_person = None
def draw_line():
    # global selected_person
    if selected_person == None:
        return
    if selected_person.order == None:
        return
    if selected_person.order.distributor == None:
        return
    pg.draw.line(screen, (0,0,0), tuple(selected_person.position), tuple(selected_person.order.distributor.position), 4)
    
def draw_label():
    # global selected_person
    if selected_restaurant == None:
        return
    show_restaurant_orders()
    #pg.draw.line(screen, (0,0,0), tuple(selected_person.position), tuple(selected_person.order.distributor.position), 4)
    



def draw_distributors(app:SimulatedApp):
    global tick
    init_draw(app)
    for distributor in app.distributors:
        posx, posy = distributor.position
        if distributor.action == Distributor.Action.Explore:
            pg.draw.circle(screen, (0,255,0), (posx, posy), 2)
        elif distributor.action == Distributor.Action.PickUpOrder:
            pg.draw.circle(screen, (255,128,0), (posx, posy), 2)
        elif distributor.action == Distributor.Action.Deliver:
            pg.draw.circle(screen, (0,0,0), (posx, posy), 2)
    draw_line()
    draw_label()
    pg.display.flip()
    RUN(tick, app)
    tick += 1


posx=22
posy=22
pg.draw.circle(screen,(0,255,0) , (posx,posy), 2)
R = pg.draw.rect(screen, (255,0,0), pg.Rect(30, 15, 10, 10),2)

myApp = INIT()

init_draw(myApp)
pg.display.update()


# s = sched.scheduler(pg.time.Clock.get_time, pg.time.wait)
s = sched.scheduler(time.time, time.sleep)
# s.enter(1, 1, draw_distributors, kwargs={'tick': local_tick, 'app': myApp})

# s.run()

# banana_delay = 500 # 0.5 seconds
banana_delay = 500 # 0.5 seconds
banana_event = pg.USEREVENT + 1
# pg.time.set_timer(banana_event, banana_delay)


# def check_event(app:SimulatedApp):
#     for event in pg.event.get():
#         if event.type == pg.MOUSEMOTION:
#             for restaurant in app.restaurants:
#                 if restaurant.rect.collidepoint(pg.mouse.get_pos()):
#                     # screen.blit(text,textRect)
#                     # x,y = pg.mouse.get_pos()
#                     # print(x,y)
#                     print(len(restaurant.currentOrders), len(restaurant.doneOrders))

# local_tick = 0

# def once_a_time(app:SimulatedApp):
#     global local_tick
#     local_tick += 1
#     draw_distributors(tick=local_tick, app=app)


tick = 0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEMOTION:
            for restaurant in myApp.restaurants:
                if restaurant.rect.collidepoint(pg.mouse.get_pos()):
                    #show_restaurant_orders(restaurant)
                    selected_restaurant = restaurant
                    # screen.blit(text,textRect)
                    # x,y = pg.mouse.get_pos()
                    # print(x,y)
                    print(len(restaurant.currentOrders), len(restaurant.doneOrders))

            for person in myApp.people:
                if person.circle.collidepoint(pg.mouse.get_pos()):
                    selected_person = person
                    # x,y = pg.mouse.get_pos()
                    # print(x,y)
                    print(person.id, person.hasOrdered, person.locked)
                    if person.order != None:
                        # person.line = pg.draw.line(screen, (0,0,0), tuple(person.position), tuple(person.order.distributor.position), 4)
                        print(person.order.id, person.order.state)
                    # line = pg.draw.line(screen, (0,0,0), (40,780), (80,720), 4)
                        # print(person.order.distributor.id, person.order.distributor.action)
                    # pg.display.flip()
        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_1):
                speed+=0.001
            elif(event.key == pg.K_2):
                speed-=0.001
            elif(event.key == pg.K_t):
                print(tick)

            #else:
                #Posiciones
                # mapa()
                # pg.display.flip()
                
    # s.enter(0.01, 1, once_a_time, kwargs={'app': myApp})
    # s.enter(0.01, 1, draw_distributors, kwargs={'app': myApp})


    
        
        



    #speed = 0.001
    s.enter(speed, 1, draw_distributors, kwargs={'app': myApp})
    # draw_line()
    s.run()
    # local_tick += 1
    # pg.display.flip()

pg.quit()