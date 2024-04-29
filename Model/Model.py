import random
from time import sleep
from Model.AristaNode import AristaNode
from Model.NodeModel import NodeModel

class Model:
    def __init__(self, population, mutation, genOrEf, isgenOrEff, circles, aristasIn, aristasOut, controlModel):
        self.population = population
        self.mutation = mutation
        self.isgenOrEff = isgenOrEff
        self.genOrEf = genOrEf        
        self.stopModel = False
        self.aristasIn = aristasIn
        self.aristasOut = aristasOut
        self.circles = circles        
        self.generation = 0
        self.aptitudeValues = []
        self.controlModel = controlModel
    
    def deactivateControlModel(self):
        self.controlModel = 0

    def initModel(self):
        if self.stopModel == False:
            self.generateFirstPopulation()
            self.runCars() # Run cars for the first population
        while not self.stopModel:
            self.controlModel.imprimir()
            sleep(3)

    def generateFirstPopulation(self):         
        #ALL Aristas need a new percentage
        #Just AristasIn always in 100%
        #Set percentage of aristasIn
        for i in range(self.population):
            if self.stopModel == False:
                self.createIndividual()

    def createIndividual(self):
        #This is to create 1 individual
        for arista in self.aristasIn:
            if isinstance(arista, AristaNode) and arista.typeArista=="in":
                arista.addNewPercentage(100)
        for circle in self.circles:
            if isinstance(circle, NodeModel):
                aristasQuantity = len(circle.aristasOut)
                totalPercentage = 0
                aristasNumber = 0
                for aristaOut in circle.aristasOut:
                    aristasNumber += 1
                    percentageToSet = self.createRandomPercentage(totalPercentage,aristasQuantity,aristasNumber,aristaOut.percentage)
                    totalPercentage += percentageToSet
                    if isinstance(aristaOut, AristaNode) and aristaOut.typeArista == "normal":
                        aristaOut.addNewPercentage(percentageToSet)
                    elif isinstance(aristaOut, AristaNode) and aristaOut.typeArista == "out":
                        aristaOut.addNewPercentage(percentageToSet)

    def runCarsForOneIndividual(self,indexIndividual):
        #Add cars to the circles beetween the aristas that enter cars
        for arista in self.aristasIn:
            if isinstance(arista, AristaNode) and arista.typeArista == "in":
                circleAddCars = arista.circle2
                if isinstance(circleAddCars, NodeModel):    
                    try:                        
                        circleAddCars.amountOfCars[indexIndividual] += (arista.capacity)
                    except IndexError:
                        circleAddCars.addCars(arista.capacity)
        #Now the circles have cars to send to the aristas
        circlesAlreadySendCars = set()
        while not set(self.circles).issubset(circlesAlreadySendCars):
            for circle in self.circles:
                if not (circle in circlesAlreadySendCars):
                    if not self.reviewNormalAristasInCircle(circle):
                        self.sendCarsToAristasOut(circle,indexIndividual)
                        circlesAlreadySendCars.add(circle)
                    elif self.reviewAllCirclesBeforeAlreadySendcars(circle,circlesAlreadySendCars,indexIndividual):
                        self.sendCarsToAristasOut(circle,indexIndividual)
                        circlesAlreadySendCars.add(circle)        
            
                
    def reviewAllCirclesBeforeAlreadySendcars(self,circle,circlesAlreadySendCars,indexIndividual):
        if isinstance(circle, NodeModel):
            if not circle.aristasIn:
                return True
            else:
                carsToAdd = 0
                for arista in circle.aristasIn:
                    if isinstance(arista, AristaNode) and arista.typeArista == "normal":
                        if not (arista.circle1 in circlesAlreadySendCars):
                            return False
                        carsToAdd += arista.amounts_of_cars[indexIndividual]
                try:
                    circle.amountOfCars[indexIndividual] = carsToAdd
                except IndexError:
                    circle.addCars(carsToAdd)
                return True

    def reviewNormalAristasInCircle(self,circle):
        if isinstance(circle, NodeModel):
            for arista in circle.aristasIn:
                if isinstance(arista, AristaNode) and arista.typeArista == "normal":
                    return True
        return False

    def sendCarsToAristasOut(self,circle,indexIndividual):
        if isinstance(circle, NodeModel):
            carsFromTheCircle = circle.amountOfCars[indexIndividual]
            for arista in circle.aristasOut:                
                self.calculateAndSendCarsToArista(arista, indexIndividual, carsFromTheCircle)
    
    def calculateAndSendCarsToArista(self, arista, indexIndividual, carsFromTheCircle):
        percetageToSend = int(arista.percentages[indexIndividual])
        capacity = arista.capacity
        # Quit the decimal using int(), round the number using round()
        carsToSend = round(carsFromTheCircle * (percetageToSend / 100))
        try:
            carsInArista = arista.amounts_of_cars[indexIndividual]
            carsThatFit = capacity - carsInArista
            if carsThatFit > 0 and not (carsThatFit >= carsToSend):
                carsToSend = abs(carsThatFit - carsToSend)
            arista.amounts_of_cars[indexIndividual] += carsToSend
        except IndexError:
            if not (capacity >= carsToSend):
                carsToSend = abs(capacity - carsToSend)
            arista.addNewAmountOfCars(carsToSend)
            
    def runCars(self):        
        #Run the cars by the percentage and capacity of the aristas
        amountCarsEnter = self.getAmountOfCarsThatEnter()
        for i in range(self.population):
            self.runCarsForOneIndividual(i)
            aptitudeValue = self.getAptitudeValueForIndividual(i,amountCarsEnter)
            if(aptitudeValue == 0):
                print("Found solution with individual: ", i)
                break


    def createRandomPercentage(self,totalPercentage,aristasQuantity,aristasNumber,minPercentage):
        if totalPercentage == 100:
            return 0
        if aristasQuantity == aristasNumber:
            return 100 - totalPercentage
        randomNumber = random.randint(minPercentage, 100-totalPercentage)
        return randomNumber

    def getAptitudeValueForIndividual(self,indexIndividual,amountCarsEnter):
        #Get amount of cars that exit
        amountCarsExit = self.getAmountOfCarsThatExitFromIndividual(indexIndividual)
        #Get amount of cars that enter = amountCarsEnter
        #Compare and that is the aptitude function
        aptitudeValue = amountCarsEnter - amountCarsExit
        #If the aptitude value is 0 the individual is ready
        return aptitudeValue

    def getAmountOfCarsThatExitFromIndividual(self,indexIndividual):
        amountCarsExit = 0
        for aristaOut in self.aristasOut:
            if isinstance(aristaOut, AristaNode) and aristaOut.typeArista == "out":
                try:
                    amountCarsExit += aristaOut.amounts_of_cars[indexIndividual]
                except IndexError:
                    aristaOut.amounts_of_cars[indexIndividual] = 0
                    amountCarsExit = amountCarsExit
        return amountCarsExit

    def getAmountOfCarsThatEnter(self):
        amountCarsEnter = 0
        for aristaEnter in self.aristasIn:
            if isinstance(aristaEnter, AristaNode) and aristaEnter.typeArista == "in":
                amountCarsEnter += aristaEnter.capacity
        return amountCarsEnter

    
    def changeStateModel(self):
        self.stopModel = not self.stopModel

    def saveModel(self):
        print("saveModel")
        #Traer el ultimo id de modelo
        #Guardar todos los circulos sin arista
        #Guardar todas las aristas con su circulos
        #ID model = autoincrement
        #ID circle = "model",idModel,"circle",circle.name
    
