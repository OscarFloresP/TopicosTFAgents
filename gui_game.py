from agent import *

import pygame as pg
import sched, time

class Game:
    def __init__(self):
        self.background_colour = (125,125,125)
        self.__start_pygame__()
        self.__gui_vars__()
        self.__gui_conf_vars__()

    def __conf_app_agent__(self, nrestaurants, npeople, ndistributors):
        # agent related
        self.myApp = INIT(nrestaurants, npeople, ndistributors)

    def __start_pygame__(self):
        pg.init()
        (self.width, self.height) = (1290, 730)
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Agents")

    def __gui_conf_vars__(self):
        self.speed = 0.001
        self.s = sched.scheduler(time.time, time.sleep)

    def __gui_vars__(self):
        self.tick = 0
        self.selected_person = None
        self.selected_restaurant = None
        self.font = pg.font.SysFont("JetBrainsMono NF", 30)
        self.running = True

    def __vis_person__(self):
        # Check to avoid crashing the app
        # global selected_person
        if self.selected_person == None:
            return
        if self.selected_person.order == None:
            return
        if self.selected_person.order.distributor == None:
            return
        # Do your thing
        pg.draw.line(self.screen, (0,0,0), \
            tuple(self.selected_person.position), \
                tuple(self.selected_person.order.distributor.position), 4)
        
    def __vis_restaurant__(self):
        # Check to avoid crashing the app
        if self.selected_restaurant == None:
            return
        # Do your thing
        text = self.font.render(str((len(self.selected_restaurant.currentOrders), \
            len(self.selected_restaurant.doneOrders))), True, (0,0,0))
        posx, posy = self.selected_restaurant.position
        textRect = text.get_rect()
        textRect.center = (posx - 20, posy)
        self.screen.blit(text,textRect)

    def __draw__(self):
        app = self.myApp
        # First: draw static things
        #   draw map
        self.screen.fill(self.background_colour)
        for i in range(24):
            pg.draw.rect(self.screen, (255,255,255), pg.Rect(0, 20+i*30, 1280, 4))   
        for i in range(43):
            pg.draw.rect(self.screen, (255,255,255), pg.Rect(20+i*30, 0, 4, 720))    
        #   draw people
        for person in app.people:
            posx, posy = person.position
            # pg.draw.circle(screen, (0,0,255), (posx, posy), 2)
            person.circle = pg.draw.circle(self.screen, (255,255,0), (posx, posy), 2)
            if person.hasOrdered:
                posx, posy = person.address
                # pg.draw.circle(screen, (255,255,0), (posx, posy), 2)
                pg.draw.circle(self.screen, (0,0,255), (posx, posy), 2)
        #   draw restaurants
        for restaurant in app.restaurants:
            posx, posy = restaurant.position
            if len(restaurant.currentOrders) >= restaurant.capacity:
                restaurant.rect = pg.draw.rect(self.screen, (255,0,0), pg.Rect(posx, posy, 10, 10), 2)
            else:
                restaurant.rect = pg.draw.rect(self.screen, (0,255,0), pg.Rect(posx, posy, 10, 10), 2)
            posx, posy = person.address
            pg.draw.circle(self.screen, (255,255,0), (posx, posy), 2)
        # Second: draw moving things
        #   draw distributors
        for distributor in app.distributors:
            posx, posy = distributor.position
            if distributor.action == Distributor.Action.Explore:
                pg.draw.circle(self.screen, (0,255,0), (posx, posy), 2)
            elif distributor.action == Distributor.Action.PickUpOrder:
                pg.draw.circle(self.screen, (255,128,0), (posx, posy), 2)
            elif distributor.action == Distributor.Action.Deliver:
                pg.draw.circle(self.screen, (0,0,0), (posx, posy), 2)
        # draw visualization functions and update screen
        self.__vis_person__()
        self.__vis_restaurant__()
        pg.display.flip()
        # Third: run logic algorithm iteration
        RUN(self.tick, app=app)
        self.tick += 1
        pg.display.set_caption("Agents | Tick: " + str(self.tick))

    def play(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEMOTION:
                    for restaurant in self.myApp.restaurants:
                        if restaurant.rect.collidepoint(pg.mouse.get_pos()):
                            self.selected_restaurant = restaurant
                            # # screen.blit(text,textRect)
                            # # x,y = pg.mouse.get_pos()
                            # # print(x,y)
                            # print(len(restaurant.currentOrders), len(restaurant.doneOrders))
                    for person in self.myApp.people:
                        if person.circle.collidepoint(pg.mouse.get_pos()):
                            self.selected_person = person
                            # # x,y = pg.mouse.get_pos()
                            # # print(x,y)
                            # print(person.id, person.hasOrdered, person.locked)
                            # if person.order != None:
                            #     # person.line = pg.draw.line(screen, (0,0,0), tuple(person.position), tuple(person.order.distributor.position), 4)
                            #     print(person.order.id, person.order.state)
                            # # line = pg.draw.line(screen, (0,0,0), (40,780), (80,720), 4)
                            #     # print(person.order.distributor.id, person.order.distributor.action)
                            # # pg.display.flip()
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_1):
                        self.speed+=0.01
                    elif(event.key == pg.K_2):
                        self.speed-=0.01
                    elif(event.key == pg.K_t):
                        print(self.tick)
            self.s.enter(self.speed, 1, self.__draw__)
            self.s.run()
        pg.quit()