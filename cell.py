from component import Component

class Cell(Component):
        def __init__(self):
            super().__init__()
            object.__setattr__(self, "rotation",0)
            object.__setattr__(self, "row", None)
            object.__setattr__(self, "col", None) 

        def interact(self,car, y, x):
              
            if self._type == 'road':
                car.speed *= 0.97 # reduce speed due to friction
                
            elif self._type == 'booster':
                car.speed += 47
                if car.speed > car.top_speed:
                    car.speed = car.top_speed

            elif self._type == 'obstacle':
                car.speed = 0

            elif self.type == 'fuel':
                 car.fuel += 10
                 if car.fuel > car.top_fuel:
                      car.fuel = car.top_fuel 

            
                


           
      

