# This controller is used to validate the percentages of Aristas And obligatory nodes

from Exceptions.ExceptionFigure import ExceptionFigure


class ControlFigures:
    def __init__(self):
        print("controlCreated")
        self.exceptions = []

    def validateAllFigures(self,aristas,circles):
        self.exceptions = []
        self.validateAristasAreAllPercentage(circles)

    
    def validateAristasAreAllPercentage(self,circles):        
        for circle in circles:
            aristas = circle.aristasOut
            totalPercentage = sum(arista.percentage for arista in aristas)
            if totalPercentage > 100:
                self.exceptions.append(ExceptionFigure("2","Aristas de nodo: , Sobrepasan el 100%" ))
            elif totalPercentage < 100:
                self.exceptions.append(ExceptionFigure("2","Aristas de nodo: , Necesitan alcanzar el 100%" ))


            
        

