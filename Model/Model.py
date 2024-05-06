import random
from time import sleep
from Model.AristaNode import AristaNode
from Model.NodeModel import NodeModel

class Model:
    def __init__(self, population, mutation, genOrEf, isgenOrEff, circles, aristasIn, aristasOut, controlModel):
        self.population = population
        self.mutation = mutation #Rate mutation came as double like, 25.0 That means 25%, or 1.15 that means 1.15%
        self.isgenOrEff = isgenOrEff
        self.genOrEf = genOrEf        
        self.stopModel = False
        self.aristasIn = aristasIn
        self.aristasOut = aristasOut
        self.circles = circles        
        self.generation = 0
        self.aptitudeValues = []
        self.controlModel = controlModel
        self.efficiency = 0
        self.genes = []
        self.indexFoundSolution = -1
        self.quantityMutations = 0
    
    def deactivateControlModel(self):
        self.controlModel = 0
    
    def updateInterfaceToInitModel(self):
        self.controlModel.updateInterfaceToInitModel(self.generation,self.efficiency,self.quantityMutations)
        

    def initModel(self):
        if not self.stopModel:
            self.generateFirstPopulation()
            self.runCars() # Run cars for the first population
        if self.isgenOrEff == "Numero de generaciones" and self.indexFoundSolution == -1:
            print("Por numero de generaciones")
            for gen in range(self.genOrEf):
                if not self.stopModel:
                    self.createNewPopulation()
                    self.generation += 1
                    self.exchangeMutation()
                    self.runCars()
                    self.updateInterfaceToInitModel()
                    if self.indexFoundSolution != -1:
                        break
                else:                    
                    break
        elif self.isgenOrEff == "Porcentaje de eficiencia" and self.indexFoundSolution == -1:
            while self.genOrEf >= self.efficiency and not self.stopModel:
                if not self.stopModel:
                    self.createNewPopulation()
                    self.generation += 1
                    self.exchangeMutation()
                    self.runCars()
                    if not self.stopModel:
                        self.updateInterfaceToInitModel()
                    if self.indexFoundSolution != -1:
                        break
                else:
                    break 
            print("Por porcentaje")
    
    def createNewPopulation(self):
        for i in range(self.population):
            for arista in self.aristasIn:
                if isinstance(arista, AristaNode) and arista.typeArista=="in":
                    arista.addNewPercentage(100)
        parents = self.selectParents()
        self.mergeParentsByPoint(parents)
        
    
    def mergeParentsByPoint(self,parents):        
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]

            pointToMerge = random.randrange(0,len(self.genes))
            indexToAdd = (self.population * (self.generation+1)) + i 

            #Add and merge the genes of the parents
            actualPoint = 0
            for gene in self.genes:
                if isinstance(gene, AristaNode):
                    percentageParent1 = gene.percentages[parent1]
                    percentageParent2 = gene.percentages[parent2]
                    if pointToMerge <= actualPoint:
                        gene.addNewPercentage(percentageParent1)
                        gene.addNewPercentage(percentageParent2)
                    else:
                        gene.addNewPercentage(percentageParent2)
                        gene.addNewPercentage(percentageParent1)
    
        
    
    def selectParents(self):
        firstIndexPopulation = (int(self.population) * (self.generation)) 
        lastIndexPopulation = (int(self.population) * (self.generation + 1)) - 1 

        #Total aptitude
        totalAptitude = self.getTotalAptitude(firstIndexPopulation,lastIndexPopulation)

        #Parents
        selectedParents = []

        for i in range(self.population):
            sumValue = 0
            #Generate the random number from 0 to totalAptitude
            randomValue = random.randrange(0, totalAptitude)
            for indexAptitudeValue in range(firstIndexPopulation, lastIndexPopulation):
                sumValue += self.aptitudeValues[indexAptitudeValue]
                if(sumValue >= randomValue):
                    selectedParents.append(indexAptitudeValue)
                    break

        #Quantity of parents = total population
        return selectedParents
    
    def getTotalAptitude(self,firstIndexPopulation,lastIndexPopulation):
        totalAptitude = 0
        for indexAptitudeValue in range(firstIndexPopulation, lastIndexPopulation):
            totalAptitude += self.aptitudeValues[indexAptitudeValue]
        
        return totalAptitude

    def exchangeMutation(self):
        #Create the random value of the parcentage to create the mutation
        percentageRandom = round(random.uniform(0, 100), 2)

        if(percentageRandom <= self.mutation):
            self.quantityMutations += 1
            firstIndexPopulation = (int(self.population) * (self.generation)) 
            lastIndexPopulation = (int(self.population) * (self.generation + 1)) - 1 
            randIndexIndividual = random.randrange(firstIndexPopulation,lastIndexPopulation)
            self.mutateIndividual(randIndexIndividual)
    
    def mutateIndividual(self,indexIndividualToMutate):
        randgen1 = random.randrange(0,len(self.genes))
        randgen2 = random.randrange(0,len(self.genes))
        aristagen1 = self.genes[randgen1]
        aristagen2 = self.genes[randgen2]
        valuegen1 = aristagen1.percentages[indexIndividualToMutate]
        valuegen2 = aristagen2.percentages[indexIndividualToMutate]
        aristagen1.percentages[indexIndividualToMutate] = valuegen2
        aristagen2.percentages[indexIndividualToMutate] = valuegen1
                

                

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
                        self.addToGenes(aristaOut)
                    elif isinstance(aristaOut, AristaNode) and aristaOut.typeArista == "out":
                        aristaOut.addNewPercentage(percentageToSet)
                        self.addToGenes(aristaOut)
    
    def addToGenes(self,arista):
        if not arista in self.genes:
            self.genes.append(arista)

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
                try:
                    carsToAdd = circle.amountOfCars[indexIndividual]
                except:
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
                carsToQuit = carsThatFit - carsToSend
                carsToSend = abs(carsToSend + carsToQuit)
            arista.amounts_of_cars[indexIndividual] += carsToSend
        except IndexError:
            if not (capacity >= carsToSend):
                carsToQuit = capacity - carsToSend
                carsToSend = abs(carsToSend + carsToQuit)
            arista.addNewAmountOfCars(carsToSend)
            
    def runCars(self):   
        #Run the cars by the percentage and capacity of the aristas
        amountCarsEnter = self.getAmountOfCarsThatEnter()
        for i in range(self.population * self.generation, self.population * (self.generation + 1) ):
            self.runCarsForOneIndividual(i)
            aptitudeValue = self.getAptitudeValueForIndividual(i)
            self.aptitudeValues.append(aptitudeValue)
            #Set the performance
            if(amountCarsEnter > 0):
                efficiencyIndividual = (aptitudeValue/amountCarsEnter) * 100
            else: 
                efficiencyIndividual = 100
            
            if(efficiencyIndividual > self.efficiency):
                self.efficiency = efficiencyIndividual

            if(aptitudeValue == amountCarsEnter):
                print("Found solution with individual: ", i)
                self.indexFoundSolution = i
                break
    
    def getEfficiencyForOneGeneration(self,generation):
        amountCarsEnter = self.getAmountOfCarsThatEnter()
        aptitudeValue = self.getAptitudeValueForIndividual(generation)
        efficiencyIndividual = (aptitudeValue/amountCarsEnter) * 100
        return efficiencyIndividual


    def createRandomPercentage(self,totalPercentage,aristasQuantity,aristasNumber,minPercentage):
        if totalPercentage == 100:
            return 0
        if aristasQuantity == aristasNumber:
            return 100 - totalPercentage
        randomNumber = random.randint(minPercentage, 100-totalPercentage)
        return randomNumber

    def getAptitudeValueForIndividual(self,indexIndividual):
        #Get amount of cars that exit
        amountCarsExit = self.getAmountOfCarsThatExitFromIndividual(indexIndividual)
        #Get amount of cars that enter = amountCarsEnter
        #Compare and that is the aptitude function
        #aptitudeValue = amountCarsEnter - amountCarsExit
        aptitudeValue = amountCarsExit
        #If the aptitude value is = amountCarsEnter the individual is ready
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

    
