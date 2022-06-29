import random as random
import time

from enum import Enum

WIDTH, HEIGHT = 1280, 720
REPORT_IN_CLI = False

# Related to the orders
class State(Enum):
    InPreparation = 1
    ReadyForDelivery = 2
    MovingOut = 3
    Delivered = 4

class Order:
    def __init__(self, person, restaurant):
        self.id = time.time()
        self.person = person
        self.restaurant = restaurant
        self.__report_init__()
        self.state = State.InPreparation
        self.distributor = None

    def __report_init__(self):
        if REPORT_IN_CLI:
            print(f"OC:{self.id},{self.person.id},{self.restaurant.id}")

    def setState(self, state:State):
        self.state = state
        if REPORT_IN_CLI:
            print(f"OS:{self.id},{self.state}")

    def setDistributor(self, distributor):
        self.distributor = distributor     

# Related to agents
class Agent:
    def __init__(self, id, distributor=False):
        self.id = id
        self.tick_primary = 0
        self.tick_secondary = 0
        self.__gen_position__(distributor)
        if not distributor:
            self.address = [self.position[0] - ((self.position[0] % 30) - 22), self.position[1]]

    def __gen_position__(self, distributor:bool):
        position = [random.randint(0, WIDTH - 21), random.randint(0, HEIGHT)]
        if distributor:
            position = [ position[0] - ((position[0] % 30) - 22),\
                position[1] - ((position[1] % 30) - 22)]   
        else:
            if ((position[0] % 30) - 22) == 0:
                position[0] +=4
            if ((position[1] % 30) - 22) == 0:
                position[1] +=4
            self.address = [position[0] - ((position[0] % 30) - 22), position[1]]
        self.position = position

    def wait_primary(self, limit_tick):
        if self.tick_primary <= limit_tick:
            self.tick_primary += 1
            return True
        self.tick_primary = 0
        return False

    def wait_secondary(self, limit_tick):
        if self.tick_secondary <= limit_tick:
            self.tick_secondary += 1
            return True
        self.tick_secondary = 0 
        return False

class Restaurant(Agent):
    def __init__(self, id):
        super().__init__(id)
        self.capacity = 10
        self.currentOrders = []
        self.doneOrders = []
        self.limit_tick = 50

    def takeOrder(self, order:Order):
        self.currentOrders.append(order)

    def prepareOrder(self):
        if len( self.currentOrders) == 0:
            return
        if self.wait_primary(250):
            return
        order: Order = self.currentOrders.pop(0)
        self.doneOrders.append( order )
        order.setState(State.ReadyForDelivery)

    def giveOrder(self, order:Order):
        # if a distributor reaches before the order is ready, he/she will wait
        if order.state == State.InPreparation:
            return False
        if self.wait_secondary(50):
            return False
        self.doneOrders.remove(order)
        return True
        
class Person(Agent):
    def __init__(self, id):
        super().__init__(id)
        self.locked = False
        self.limit = random.choice([1000, 10_000])
        self.__reset_vars__()

    def __reset_vars__(self):
        self.hasOrdered = False
        self.order = None

    def __unlock__(self):
        if self.wait_primary(self.limit):
            return
        self.locked = False

    def requestOrder(self, app):
        if len(app.restaurants) == 0:
            return
        if self.locked:
            self.__unlock__()
            return
        app.takeOrder(self, random.choice(app.restaurants))


    def receiveConfirmation(self, order=None):
        if order == None:
            self.__reset_vars__()
            self.locked = True
            return
        self.hasOrdered = True
        self.order = order
        

class Distributor(Agent):
    class Action(Enum):
        Explore = 1
        PickUpOrder = 2
        Deliver = 3

    class Direction(Enum):
        Up = 1
        Dw = 2

    def __init__(self, id):
        super().__init__(id, distributor=True)
        self.notifications = []
        self.direction = self.Direction(random.randint(1, 2))
        self.__reset_vars__()
    
    def __reset_vars__(self):
        self.action = self.Action.Explore
        self.order = None

    # SIMULATE THE SYSTEM OF NOTFICATIONS FROM THE APP
    def __AutoReceiveNotification__(self, notification:Order):
        self.notifications.append( notification )

    def __AutoRemoveNotification__(self, notification:Order):
        # self.notifications.remove( notification )
        try:
            self.notifications.remove( notification )
        except:
            pass

    # ACTUAL METHODS
    def isAvailable(self):
        return self.action == self.Action.Explore

    # WARNING WARNING WARNING
    def takeOrder(self, app):
        if not self.isAvailable():
            return
        if len( self.notifications ) == 0:
            return
        if self.wait_primary(150):
            return
        order = self.notifications.pop(0)
        app.answerFromDistributor(self, order) # Request the app to deliver the order

    def receiveConfirmation(self, order=None):
        self.action = self.Action.PickUpOrder
        self.order = order
        if REPORT_IN_CLI:
            print(f"DT:{self.id},{self.order.id}")
            
    def __explore__(self):
        which = random.randint(0, 1)
        if which == 0:
            which = 0 if ((self.position[1] % 30) - 22 == 0) else 1
        elif which == 1:
            which = 1 if ((self.position[0] % 30) - 22 == 0) else 0
        movement = (-1)**random.randint(0, 1)
        self.position[which] += movement
        if self.position[which] > (WIDTH if which else HEIGHT):
            self.position[which] -= movement
        elif self.position[which] < 0:
            self.position[which] -= movement

    def __moveTo__(self, position):

        minimum_movement = 1
        # move in 0 axis
        allowed_in_0 = ((self.position[1] % 30) - 22 == 0)
        if allowed_in_0:
            if position[0] > self.position[0]:
                self.position[0] += minimum_movement
                if self.position[0] > WIDTH:
                    self.position[0] -= minimum_movement
                return
            elif position[0] < self.position[0]:
                self.position[0] -= minimum_movement
                if self.position[0] < 0:
                    self.position[0] -= minimum_movement
                return
        # move in 1 axis
        allowed_in_1 = ((self.position[0] % 30) - 22 == 0)
        if allowed_in_1:
            if allowed_in_0:
                if position[1] > self.position[1]:
                    self.direction = self.Direction.Dw
                elif position[1] < self.position[1]:
                    self.direction = self.Direction.Up
            if position[0] == self.position[0] and position[1] == self.position[1]:
                pass
            elif self.direction == self.Direction.Up:
                self.position[1] -= minimum_movement
                return
            elif self.direction == self.Direction.Dw:
                self.position[1] += minimum_movement
                return

        # if reach here, then it has arrived

        order: Order = self.order
        if self.action == self.Action.PickUpOrder:
            if order.restaurant.giveOrder(self.order):
                order.setState(State.MovingOut)
                self.action = self.Action.Deliver
        elif self.action == self.Action.Deliver:
            order.person.receiveConfirmation(None) # give the order to the person and reset
            order.setState(State.Delivered)
            self.__reset_vars__()

    def move(self):
        lastPosition = self.position[::]

        if self.action == self.Action.Explore:
            self.__explore__()
            return
        else:
            order:Order = self.order
            if self.action == self.Action.PickUpOrder:
                self.__moveTo__(order.restaurant.address)
            elif self.action == self.Action.Deliver:
                self.__moveTo__(order.person.address)

        if REPORT_IN_CLI:
            print(f"DM:{self.id},{lastPosition},{self.position}")

# Simulate the app
class SimulatedApp:
    def __init__(self, restaurants, people, distributors):
        self.restaurants = restaurants
        self.people = people
        self.distributors = distributors
        self.orders = []

    def askForDistributor(self, order:Order):
        [ d.__AutoReceiveNotification__(order) for d in self.distributors ]

    # WARNING WARNING
    def answerFromDistributor(self, distributor:Distributor, order:Order):
        order.setDistributor(distributor)
        distributor.receiveConfirmation(order)
        # THEN
        [ d.__AutoRemoveNotification__(order) for d in self.distributors ]

    def takeOrder(self, person:Person, restaurant:Restaurant):
        if person.hasOrdered:
            if REPORT_IN_CLI:
                print(f"PH:{person.id}") # has already ordered
            return
        elif len(restaurant.currentOrders) < restaurant.capacity:
            # CRITICAL SECTION
            order = Order(person, restaurant) # create the order
            restaurant.takeOrder(order) # makes restaurant take the order
            person.receiveConfirmation(order) # put to wait the person
            # THEN
            self.askForDistributor(order)
        else:
            if REPORT_IN_CLI:
                print(f"RE:{restaurant.id},{person.id}") # restaurant will exceed capacity
            return

def INIT(nrestaurants=100, npeople=2000, ndistributors=300):
    rs = [ Restaurant("R" + str(i + 1)) for i in range(nrestaurants)]
    ps = [ Person("P" + str(i + 1)) for i in range(npeople)]
    ds = [ Distributor("D" + str(i + 1)) for i in range(ndistributors) ]

    return SimulatedApp(rs, ps, ds)

def RUN(tick, app):
    if REPORT_IN_CLI:
        print(f"T:{tick}")

    lsps_filtered = [e for e in app.people if not e.hasOrdered ]
    [ p.requestOrder( app) for p in lsps_filtered ]

    [ d.takeOrder(app) for d in app.distributors ]

    [ d.move() for d in app.distributors ]
    [ r.prepareOrder() for r in app.restaurants ]
    # ==========================================

if __name__ == "__main__":

    myApp = INIT()

    local_tick = 0
    for i in range(1000):
        RUN(local_tick, myApp)
        local_tick += 1
