# This controller is used to validate the percentages of Aristas And obligatory nodes

from Exceptions.ExceptionFigure import ExceptionFigure


class ControlFigures:
    def __init__(self):
        print("controlCreated")
        self.exceptions = []

    def validateAllFigures(self,aristasIn,aristasOut,aristas,circles):
        self.exceptions = []
        #self.validateAristasAreAllPercentage(circles)
        if len(aristas) == 0:
            self.exceptions.append(ExceptionFigure("2","Hay que agregar aristas normales" ))
        if len(aristasIn) == 0:
            self.exceptions.append(ExceptionFigure("2","Se necesitan Aristas de entrada" ))
        if len(aristasOut) == 0:
            self.exceptions.append(ExceptionFigure("2","Se necesitan Aristas de salida " ))


    
    def validateAristasAreAllPercentage(self,circles):        
        for circle in circles:
            aristas = circle.aristasOut
            totalPercentage = sum(arista.percentage for arista in aristas)
            if totalPercentage > 100:
                self.exceptions.append(ExceptionFigure("2","Aristas de nodo: , Sobrepasan el 100%" ))
            elif totalPercentage < 100:
                self.exceptions.append(ExceptionFigure("2","Aristas de nodo: , Necesitan alcanzar el 100%" ))
        
        


            
        

