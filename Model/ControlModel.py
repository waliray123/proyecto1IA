import os
import pickle
import random
from Figures.AristaIn import AristaIn
from Figures.AristaOutput import AristaOutput
from Figures.Arista import Arista
from Figures.Circle import Circle
from Model.AristaNode import AristaNode
from Model.Model import Model
from Model.NodeModel import NodeModel


class ControlModel:
    def __init__(self, circles,interfaz):
        self.aristasIn = []
        self.aristasOut = []
        self.circles = []
        self.createNodesAndAristas(circles)
        self.interfaz = interfaz
        print("terminados")
    
    def createNodesAndAristas(self,circles):
        circlesAdded = []
        aristasAdded = []
        aristasNodeAdded = []
        for circle in circles:
            if isinstance(circle, Circle):
                nodeToInsert = NodeModel(circle.x,circle.y,"black",circle.name)
                self.circles.append(nodeToInsert)
                circlesAdded.append(circle)
                for aristaIn in circle.aristasIn:
                    indexAristaAdded = self.searchAristaInAristasAdded(aristasAdded,aristaIn)
                    if indexAristaAdded == -1:
                        #Crear arista
                        if isinstance(aristaIn, Arista):
                            aristaInsert = AristaNode("normal",aristaIn.capacity,aristaIn.percentage)
                        elif isinstance(aristaIn, AristaIn):
                            aristaInsert = AristaNode("in",aristaIn.capacity,aristaIn.percentage)
                            self.aristasIn.append(aristaInsert)

                        aristasAdded.append(aristaIn)
                        aristasNodeAdded.append(aristaInsert)
                        nodeToInsert.addAristaIn(aristaInsert)
                        aristaInsert.setCircle2(nodeToInsert)
                    else:
                        #Insertar la arista
                        aristaInsert = aristasNodeAdded[indexAristaAdded]
                        nodeToInsert.addAristaIn(aristaInsert)
                        aristaInsert.setCircle2(nodeToInsert)
                
                for aristaOut in circle.aristasOut:
                    indexAristaAdded = self.searchAristaInAristasAdded(aristasAdded,aristaOut)
                    if indexAristaAdded == -1:
                        #Crear arista
                        if isinstance(aristaOut, Arista):
                            aristaInsert = AristaNode("normal",aristaOut.capacity,aristaOut.percentage)
                        elif isinstance(aristaOut, AristaOutput):
                            aristaInsert = AristaNode("out",aristaOut.capacity,aristaOut.percentage)
                            self.aristasOut.append(aristaInsert)

                        aristasAdded.append(aristaOut)
                        aristasNodeAdded.append(aristaInsert)
                        nodeToInsert.addAristaOut(aristaInsert)
                        aristaInsert.setCircle1(nodeToInsert)
                    else:
                        #Insertar la arista
                        aristaInsert = aristasNodeAdded[indexAristaAdded]
                        nodeToInsert.addAristaOut(aristaInsert)
                        aristaInsert.setCircle1(nodeToInsert)


    def searchAristaInAristasAdded(self,aristasAdded,aristaToFind):
        indexArista = 0
        for aristaAdded in aristasAdded:
            if aristaToFind == aristaAdded:
                return indexArista
            indexArista += 1
        return -1                    
    
    def cleanModel(self):
        for arista in self.aristasIn:
            if isinstance(arista, AristaIn):
                arista.cleanArista()
        for circle in self.circles:
            if isinstance(circle, Circle):
                circle.cleanCircle()
                for aristaOut in circle.aristasOut:
                    if isinstance(aristaOut, Arista):
                        aristaOut.cleanArista()
                    elif isinstance(aristaOut, AristaOutput):
                        aristaOut.cleanArista()
    
    def initModel(self,population, mutation, genOrEf, isgenOrEff):
        self.model = Model(population, mutation, genOrEf, isgenOrEff,self.circles,self.aristasIn,self.aristasOut,self)
        self.model.initModel()
        self.model.deactivateControlModel()
        self.saveModel(self.model)
    
    def imprimir(self):
        print("imprimir desde control llamado desde modelo")
    
    def changeStateModel(self):
        print("pausadoControlModelo")
        self.model.changeStateModel()

    def saveModel(self, model):
        directorio = "../Proyecto1IA/Saves/"
        nombre_base = "model"
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        if os.path.exists(directorio + nombre_base + ".mdl"):
            contador = 1
            while True:
                ruta_archivo = f"{directorio}{nombre_base}_{contador}.mdl"
                if not os.path.exists(ruta_archivo):
                    break
                contador += 1
        else:
            ruta_archivo = directorio + nombre_base + ".mdl"
        
        with open(ruta_archivo, "wb") as archivo:
            pickle.dump(model, archivo)
        
        print("Objeto guardado correctamente en", ruta_archivo)
        self.interfaz.modeloTerminadoDialog(ruta_archivo)
    
    def updateInterfaceToInitModel(self,generationnum,bestefficiency,quantitymutations):
        self.interfaz.updateInterfaceToInitModel(generationnum,bestefficiency,quantitymutations,"Modelo")
        
    


    