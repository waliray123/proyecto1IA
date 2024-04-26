import random
from Figures.AristaIn import AristaIn
from Figures.AristaOutput import AristaOutput
from Figures.Arista import Arista
from Figures.Circle import Circle


class Model:
    def __init__(self, population, mutation, genOrEf, isgenOrEff, circles, aristasIn):
        self.population = population
        self.mutation = mutation
        self.isgenOrEff = isgenOrEff
        self.genOrEf = genOrEf        
        self.circles = circles
        self.aristasIn = aristasIn
        self.stopModel = False
        self.cleanModel()
        self.initModel()
    
    def cleanModel(self):
        for arista in self.aristasIn:
            if isinstance(arista, AristaIn):
                arista.cleanArista()
        for circle in self.circles:
            if isinstance(circle, Circle):
                for aristaOut in circle.aristasOut:
                    if isinstance(aristaOut, Arista):
                        aristaOut.cleanArista()
                    elif isinstance(aristaOut, AristaOutput):
                        aristaOut.cleanArista()
        
    
    def initModel(self):
        if self.stopModel == False:
            self.generateFirstPopulation()

    def generateFirstPopulation(self):         
        #ALL Aristas need a new percentage
        #Just AristasIn always in 100%
        #Set percentage of aristasIn
        for i in range(self.population):
            self.createIndividual()

    def createIndividual(self):
        #This is to create 1 individual
        for arista in self.aristasIn:
            if isinstance(arista, AristaIn):
                arista.addNewPercentage(100)
        for circle in self.circles:
            if isinstance(circle, Circle):
                aristasQuantity = len(circle.aristasOut)
                totalPercentage = 0
                aristasNumber = 0
                for aristaOut in circle.aristasOut:
                    aristasNumber += 1
                    percentageToSet = self.createRandomPercentage(totalPercentage,aristasQuantity,aristasNumber)
                    totalPercentage += percentageToSet
                    if isinstance(aristaOut, Arista):
                        aristaOut.addNewPercentage(percentageToSet)
                    elif isinstance(aristaOut, AristaOutput):
                        aristaOut.addNewPercentage(percentageToSet)

    def createRandomPercentage(self,totalPercentage,aristasQuantity,aristasNumber):
        if totalPercentage == 100:
            return 0
        if aristasQuantity == aristasNumber:
            return 100 - totalPercentage
        randomNumber = random.randint(0, 100)
        while((totalPercentage + randomNumber) > 100):
            randomNumber = random.randint(0, 100)            
        return randomNumber
    
    def runCars(self):
        print("runCars")
        #Run the cars by the percentage and capacity of the aristas
    
    def changeStateModel(self):
        self.stopAllModel = not self.stopAllModel
    