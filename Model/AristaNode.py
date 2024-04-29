class AristaNode:
    def __init__(self,typeArista,capacity,percentage):
        self.typeArista = typeArista
        self.capacity = capacity
        self.percentage = percentage
        self.percentages = []
        self.amounts_of_cars = []

    def setCircle1(self,circle1):
        self.circle1 = circle1
    
    def setCircle2(self,circle2):
        self.circle2 = circle2
    
    def addNewPercentage(self,newPercentage):
        self.percentages.append(newPercentage)
    
    def addNewAmountOfCars(self,amount_of_cars):
        self.amounts_of_cars.append(amount_of_cars)

    def cleanArista(self):
        self.percentages = []
        self.amounts_of_cars = []