from component import Component

class Car(Component):

    def __init__(self, model):
        self.model = model
        self.top_speed = 0
        self.speed = 0
        self.driver = None
        self.pos = (0, 0)
        self.map = None
        self.angle = 0
        self.fuel = 100
        self.max_fuel = 100
        self.decel = 111
        self.left = False
        self.right = False
        self.accel_flag = False

        if self.model == 'Ferrari':
            self.accel = 50
        elif self.model == 'BMW':
            self.accel = 44
        elif self.model == 'Mercedes-Benz':
            self.accel = 43
        elif self.model == 'Bugatti':
            self.accel = 61
        elif self.model == 'Koenigsegg':
            self.accel = 63
        elif self.model == 'Lamborghini':
            self.acccel = 51
        elif self.model == "McLaren":
            self.accel = 50

        if self.model == 'Ferrari':
            self.top_sepeed = 370
        elif self.model == 'BMW':
            self.top_sepeed = 305  
        elif self.model == 'Mercedes-Benz':
            self.top_sepeed = 310
        elif self.model == 'Bugatti':    
            self.top_sepeed = 485
        elif self.model == 'Koenigsegg':
            self.top_sepeed = 490
        elif self.model == 'Lamborghini':
            self.top_speed = 350
        elif self.model == "McLaren":
            self.top_sepeed = 400

    def stop(self):
        while self.speed >= 0:
            self.speed -= 0

        if self.speed <= 0:
            self.speed = 0

        