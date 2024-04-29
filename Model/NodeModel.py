class NodeModel:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.amountOfCars = []
        self.aristasOut = []
        self.aristasIn = []
    
    def addCars(self,amountOfCars):
        self.amountOfCars.append(amountOfCars)

    def cleanCircle(self):
        self.amountOfCars = []
    
    def addAristaIn(self,aristaIn):
        self.aristasIn.append(aristaIn)
    
    def addAristaOut(self,aristaOut):
        self.aristasOut.append(aristaOut)
