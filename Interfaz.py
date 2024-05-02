import pickle
import threading
import tkinter as tk
from tkinter import filedialog


from Figures.Arista import Arista
from Figures.AristaOutput import AristaOutput
from Figures.AristaIn import AristaIn
from Figures.Circle import Circle
from Controllers.controlFigures import ControlFigures
from Model.AristaNode import AristaNode
from Model.ControlModel import ControlModel
from Model.Model import Model
from Model.NodeModel import NodeModel

class Interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplicación")
        self.canvas = tk.Canvas(self.root, width=1400, height=600, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)  # Ajusta la posición según tu diseño

        self.label_estado = tk.Label(self.root, text="")
        self.label_estado.grid(row=1, column=0, columnspan=4)  # Ajusta la posición según tu diseño

        self.boton_terminar_arista = tk.Button(self.root, text="Terminar Arista", command=self.crear_arista)
        self.boton_terminar_arista.grid(row=2, column=0, columnspan=4)  # Ajusta la posición según tu diseño
        self.boton_terminar_arista.grid_remove()

        self.createInterfaceToInitModel()
        #self.boton_parar_modelo.grid_remove()

        self.initValues()

        self.createConfigLabels()
    
    def initValues(self):
        self.circles = []
        self.aristas = []
        self.aristasIn = []
        self.aristasOut = []
        self.selected_circles = []
        self.creando_arista = False
        self.borrando_arista = False
        self.borrando_nodo = False
        self.actualizando_arista = False
        self.creando_arista_salida = False
        self.creando_arista_entrada = False

        self.controlFigures = ControlFigures()
        self.nameNode = 0    
        self.population_size = 0
        self.mutation_rate = 0
        self.generation_or_efficiency = 0
        self.value_generation_or_efficiency = 0
    
    def createInterfaceToInitModel(self):
        self.boton_parar_modelo = tk.Button(self.root, text="Parar Modelo", command=self.stopModel)
        self.boton_parar_modelo.grid(row=3, column=1, columnspan=4)
        self.label_generation = tk.Label(self.root, text="Genaracion No. ")
        self.label_generation.grid(row=3, column=1, sticky="w")
        self.label_best_aptitude = tk.Label(self.root, text="Mejor Eficiencia: ")
        self.label_best_aptitude.grid(row=4, column=1, sticky="w")
        self.label_quantity_mutations = tk.Label(self.root, text="Mutaciones: ")
        self.label_quantity_mutations.grid(row=5, column=1, sticky="w")
        self.label_quantity_mutations = tk.Label(self.root, text="Seleccion Generacion: ")
        self.label_quantity_mutations.grid(row=6, column=1, sticky="w")
        self.entry_num_generation = tk.Entry(self.root)
        self.entry_num_generation.grid(row=6, column=1, sticky="s")
        self.button_validate_num_generation = tk.Button(self.root, text="Cargar", command=self.validate_num_generation)
        self.button_validate_num_generation.grid(row=6, column=1, sticky="e")

    def validate_num_generation(self):
        self.createNewCanvasModelGeneration(self.modelo_cargado,int(self.entry_num_generation.get()))
        print("validate num generation")
    
    def updateInterfaceToInitModel(self,generationnum,bestefficiency,quantitymutations):
        self.label_generation.config(text="Genaracion No. " + str(generationnum))        
        self.label_best_aptitude.config(text="Mejor Eficiencia: " + str(bestefficiency))
        self.label_quantity_mutations.config(text="Mutaciones: " + str(quantitymutations))

    
    def stopModel(self):
        self.controlmodel.changeStateModel()
        self.modelo_thread.join()

    def createConfigLabels(self):
        self.label_population = tk.Label(self.root, text="Poblacion: ")
        self.label_population.grid(row=3, column=0, sticky="w")  # Alineado a la izquierda

        self.label_mutation = tk.Label(self.root, text="Tasa de Mutacion: ")
        self.label_mutation.grid(row=4, column=0, sticky="w")  # Alineado a la izquierda

        self.label_end = tk.Label(self.root, text="Criterio de finalizacion: ")
        self.label_end.grid(row=5, column=0, sticky="w")  # Alineado a la izquierda

        self.label_end_value = tk.Label(self.root, text="Valor de Criterio de Finalizacion: ")
        self.label_end_value.grid(row=6, column=0, sticky="w")  # Alineado a la izquierda
    
    
    def updateConfigLabels(self, population, mutation, genOrEff, valueGenOrEff):
        self.label_population.config(text="Poblacion: " + population)
        self.label_mutation.config(text="Tasa de Mutacion: " + mutation)
        self.label_end.config(text="Criterio de finalizacion: " + genOrEff)
        self.label_end_value.config(text="Valor de Criterio de Finalizacion: " + valueGenOrEff)

    def toggle_creacion_arista(self):
        self.creando_arista = not self.creando_arista
        if self.creando_arista:
            self.label_estado.config(text="Modo creación de arista activado. Seleccione dos nodos.")
            self.boton_terminar_arista.grid()
            for circle in self.circles:
                self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.grid_remove()
            for circle in self.circles:
                self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
    
    def select_circle_for_arista(self, event, circle):
        circle.toggle_selection()
        if circle.selected:
            self.selected_circles.append(circle)
        else:
            self.selected_circles.remove(circle)
        if len(self.selected_circles) == 2:
            self.crear_arista()
    
    def crear_arista(self):
        circle1, circle2 = self.selected_circles
        arista = Arista(self.canvas, circle1, circle2)
        self.aristas.append(arista)
        circle1.aristasOut.append(arista)
        circle2.aristasIn.append(arista)
        self.selected_circles.clear()
        for circle in self.circles:
            circle.selected = False
            circle.canvas.itemconfig(circle.shape, outline="black", width=1)
        self.creando_arista = False
        self.label_estado.config(text="Creación de arista finalizada.")
        self.boton_terminar_arista.grid_remove()

    def crear_arista_salida(self, circle1):
        arista_salida = AristaOutput(self.canvas, circle1)
        self.aristasOut.append(arista_salida)
        circle1.aristasOut.append(arista_salida)
        arista_salida.circle2.aristasIn.append(arista_salida)
        self.creando_arista_salida = False
        self.label_estado.config(text="")        
        self.canvas.tag_bind(arista_salida.circle2.shape, "<B1-Motion>", lambda event, circle=arista_salida.circle2: circle.move(event))

        for circle in self.circles:
            self.canvas.tag_unbind(circle.shape, "<Button-1>")
    
    def crear_arista_entrada(self, circle2):
        arista_entrada = AristaIn(self.canvas, circle2)
        self.aristasIn.append(arista_entrada)
        circle2.aristasIn.append(arista_entrada)
        arista_entrada.circle1.aristasOut.append(arista_entrada)
        self.creando_arista_entrada = False
        self.label_estado.config(text="")        
        self.canvas.tag_bind(arista_entrada.circle1.shape, "<B1-Motion>", lambda event, circle=arista_entrada.circle1: circle.move(event))

        for circle in self.circles:
            self.canvas.tag_unbind(circle.shape, "<Button-1>")

    def toggle_creacion_arista_entrada(self):
        self.creando_arista_entrada = not self.creando_arista_entrada
        if self.creando_arista_entrada:            
            self.label_estado.config(text="Modo creación de arista de salida activado. Seleccione un nodo.")
            for circle in self.circles:
                self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: self.crear_arista_entrada(circle))
        else:
            self.label_estado.config(text="")            
            for circle in self.circles:
                self.canvas.tag_unbind(circle.shape, "<Button-1>")

    def toggle_creacion_arista_salida(self):
        self.creando_arista_salida = not self.creando_arista_salida
        if self.creando_arista_salida:            
            self.label_estado.config(text="Modo creación de arista de salida activado. Seleccione un nodo.")
            for circle in self.circles:
                self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: self.crear_arista_salida(circle))
        else:
            self.label_estado.config(text="")            
            for circle in self.circles:
                self.canvas.tag_unbind(circle.shape, "<Button-1>")
    
    def borrar_arista(self):
        if not self.borrando_arista:
            self.label_estado.config(text="Modo borrado de arista activado. Seleccione una arista para borrar.")
            self.boton_terminar_arista.grid_remove()
            for circle in self.circles:
                circle.selected = False
                circle.canvas.itemconfig(circle.shape, width=1)
            self.borrando_arista = True
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.grid_remove()
            self.borrando_arista = False

    def borrar_arista_seleccionada(self, event):
        if self.borrando_arista:
            arista_id = event.widget.find_closest(event.x, event.y)    
            print('aristaid:' + str(arista_id))               
            arista_found_normal = self.found_arista_selected(self.aristas,arista_id,event)
            arista_found_in = self.found_arista_selected(self.aristasIn,arista_id,event)
            arista_found_out = self.found_arista_selected(self.aristasOut,arista_id,event)
            if arista_found_out != None:
                event.widget.delete(arista_found_out.circle2.shape)      
            if arista_found_in != None:
                event.widget.delete(arista_found_in.circle1.shape)        

    
    def found_arista_selected(self,aristas,arista_id,event):
        if arista_id and arista_id[0] in [arista.arrow for arista in aristas]:
            arista = next(arista for arista in aristas if arista.arrow == arista_id[0])
            aristas.remove(arista)
            event.widget.delete(arista.arrow)
            event.widget.delete(arista.capacity_text)
            event.widget.delete(arista.percentage_text)
            for circle in self.circles:
                    if arista in circle.aristasIn:
                        circle.aristasIn.remove(arista)                        
                    if arista in circle.aristasOut:
                        circle.aristasOut.remove(arista)                        
            self.label_estado.config(text="Arista borrada. Modo borrado de arista desactivado.")    
            return arista
        return None    


    def crear_nodo(self):
        self.nameNode += 1
        circle = Circle(self.canvas, 50, 50, "white",str(self.nameNode))
        self.circles.append(circle)
        self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
        self.canvas.tag_bind(circle.shape, "<B1-Motion>", lambda event, circle=circle: circle.move(event))
        self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event: self.borrar_nodo_seleccionado(event))


    def toggle_borrado_nodo(self):
        if not self.borrando_nodo:
            self.label_estado.config(text="Modo borrado de nodo activado. Seleccione un nodo para borrar.")
            self.boton_terminar_arista.grid_remove()
            self.borrando_nodo = True
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.grid_remove()
            self.borrando_nodo = False

    def borrar_nodo_seleccionado(self, event):
        if self.borrando_nodo:
            circle_id = event.widget.find_closest(event.x, event.y)
            if circle_id and circle_id[0] in [circle.shape for circle in self.circles]:
                circle = next(circle for circle in self.circles if circle.shape == circle_id[0])
                self.circles.remove(circle)
                event.widget.delete(circle.shape)
                event.widget.delete(circle.name_text)
                for arista in circle.aristasIn:
                    self.aristas.remove(arista)
                    self.aristasIn.remove(arista)
                    event.widget.delete(arista.arrow)
                for arista in circle.aristasOut:
                    self.aristas.remove(arista)
                    event.widget.delete(arista.arrow)
                self.label_estado.config(text="Nodo borrado. Modo borrado de nodo desactivado.")
                self.borrando_nodo = False
    
    def toggle_actualizando_arista(self):
        if not self.actualizando_arista:
            self.label_estado.config(text="Modo actualización de arista activado. Seleccione una arista.")
            for arista in self.aristas:
                self.canvas.tag_bind(arista.arrow, "<Button-1>", lambda event, arista=arista: self.seleccion_arista_actualizar(arista))
            for aristaIn in self.aristasIn:
                self.canvas.tag_bind(aristaIn.arrow, "<Button-1>", lambda event, aristaIn=aristaIn: self.seleccion_arista_actualizar(aristaIn))
            for aristaOut in self.aristasOut:
                self.canvas.tag_bind(aristaOut.arrow, "<Button-1>", lambda event, aristaOut=aristaOut: self.seleccion_arista_actualizar(aristaOut))
            self.actualizando_arista = True
    
    def seleccion_arista_actualizar(self,arista):
        self.arista_actualizar = arista        
        formulario = tk.Toplevel()
        formulario.title("Actualizar Arista")
    
        capacidad_label = tk.Label(formulario, text="Capacidad:")
        capacidad_label.grid(row=0, column=0, padx=5, pady=5)
        capacidad_entry = tk.Entry(formulario)
        capacidad_entry.grid(row=0, column=1, padx=5, pady=5)
    
        tiempo_label = tk.Label(formulario, text="% Tiempo:")
        tiempo_label.grid(row=1, column=0, padx=5, pady=5)
        tiempo_entry = tk.Entry(formulario)
        tiempo_entry.grid(row=1, column=1, padx=5, pady=5)
    
        def actualizar_arista():
            capacidad = capacidad_entry.get()
            tiempo = tiempo_entry.get()
            arista.setNewProperties(capacidad,tiempo)
    
            formulario.destroy()
    
        actualizar_button = tk.Button(formulario, text="Actualizar", command=actualizar_arista)
        actualizar_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.label_estado.config(text="")
        for aristaN in self.aristas:
                self.canvas.tag_unbind(aristaN.arrow, "<Button-1>")
        for aristaIn in self.aristasIn:
                self.canvas.tag_unbind(aristaIn.arrow, "<Button-1>")
        for aristaOut in self.aristasOut:
                self.canvas.tag_unbind(aristaOut.arrow, "<Button-1>")
        self.actualizando_arista = False


    def formInitModel(self):
        formulario = tk.Toplevel()
        formulario.title("Ingreso de Valores de Modelo")
    
        population_label = tk.Label(formulario, text="Tamaño Poblacion:")
        population_label.grid(row=0, column=0, padx=5, pady=5)
        population_entry = tk.Entry(formulario)
        population_entry.grid(row=0, column=1, padx=5, pady=5)

        mutation_label = tk.Label(formulario, text="Tasa de Mutacion:")
        mutation_label.grid(row=1, column=0, padx=5, pady=5)
        mutation_entry = tk.Entry(formulario)
        mutation_entry.grid(row=1, column=1, padx=5, pady=5)        

        aditional_label = tk.Label(formulario, text="Número de generaciones:")
        aditional_label.grid(row=3, column=0, padx=5, pady=5)
        aditional_entry = tk.Entry(formulario)
        aditional_entry.grid(row=3, column=1, padx=5, pady=5)

        def mostrar_campo_adicional(selected_option):            
            if selected_option == "Numero de generaciones":
                aditional_label.config(text="Número de generaciones:")
                aditional_entry.grid(row=3, column=1)
            elif selected_option == "Porcentaje de eficiencia":
                aditional_label.config(text="Porcentaje de eficiencia:")
                aditional_entry.grid(row=3, column=1)

        finish_criteria = tk.StringVar(formulario)
        finish_criteria.set("Numero de generaciones")
        
        finish_label = tk.Label(formulario, text="Criterio de finalización:")
        finish_label.grid(row=2, column=0, padx=5, pady=5)
        finish_entry = tk.OptionMenu(formulario, finish_criteria, "Numero de generaciones", "Porcentaje de eficiencia", command=mostrar_campo_adicional)
        finish_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def insertData():    
            #DATA FORM FORM
            self.population_size = int(population_entry.get())
            self.mutation_rate = int(mutation_entry.get())
            self.generation_or_efficiency = finish_criteria.get()
            self.value_generation_or_efficiency = int(aditional_entry.get())
            self.updateConfigLabels(population_entry.get(),mutation_entry.get(),finish_criteria.get(),aditional_entry.get())
            formulario.destroy()
    
        actualizar_button = tk.Button(formulario, text="Ingresar", command=insertData)
        actualizar_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.label_estado.config(text="")
        for aristaN in self.aristas:
                self.canvas.tag_unbind(aristaN.arrow, "<Button-1>")
        for aristaIn in self.aristasIn:
                self.canvas.tag_unbind(aristaIn.arrow, "<Button-1>")
        for aristaOut in self.aristasOut:
                self.canvas.tag_unbind(aristaOut.arrow, "<Button-1>")
        self.actualizando_arista = False

    def initModel(self):
        self.controlFigures.validateAllFigures(self.aristasIn, self.aristasOut, self.aristas, self.circles)
        for exception in self.controlFigures.exceptions:
            print(exception.message)
        if not self.controlFigures.exceptions:                        
            isValidate = self.validateInformation()
            if isValidate:
                self.controlmodel = ControlModel(self.circles,self)
                self.modelo_thread = threading.Thread(target=self.controlmodel.initModel, args=(self.population_size, self.mutation_rate, self.value_generation_or_efficiency, self.generation_or_efficiency))
                self.modelo_thread.start()
    
    def cleanCanvas(self):
        self.canvas.delete("all")
        self.initValues()
                

    def saveDataFromModel(self):
        self.formInitModel()
    
    def validateInformation(self):
        if self.population_size != 0 and self.mutation_rate != 0 and self.value_generation_or_efficiency != 0:
            return True
        return False
    
    def loadModel(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.modelo_cargado = pickle.load(f)
                if isinstance(self.modelo_cargado, Model):
                    self.updateInterfaceToInitModel(self.modelo_cargado.generation,self.modelo_cargado.efficiency,self.modelo_cargado.quantityMutations)
                    self.createNewCanvasModelGeneration(self.modelo_cargado,0)
                print("Modelo cargado correctamente.")
        except FileNotFoundError:
            print("El archivo especificado no se encuentra.")
        except Exception as e:
            print("Error al cargar el modelo:", e)    
    
    
    def createNewCanvasModelGeneration(self,model,generation):        
        if isinstance(model,Model):
            self.cleanCanvas()
            #Create all Circles
            for node in model.circles:
                if isinstance(node,NodeModel):
                    self.crear_nodo_cargado(node)
            #Already created all circles
            aristasCreated = []
            for node in model.circles:
                for aristaIn in node.aristasIn:
                        if not aristaIn in aristasCreated:
                            self.crear_arista_cargado(aristaIn,generation)
                            aristasCreated.append(aristaIn)
                for aristaOut in node.aristasOut:
                        if not aristaOut in aristasCreated:
                            self.crear_arista_cargado(aristaOut,generation)
                            aristasCreated.append(aristaOut)

    
    def crear_arista_cargado(self,aristaNode,generation):
        if aristaNode.typeArista == "in":
            arista = self.create_arista_in_cargado(aristaNode,generation)
            arista.setNewProperties2(aristaNode.capacity,aristaNode.percentages[generation],aristaNode.capacity)
        elif aristaNode.typeArista == "out":
            arista = self.create_arista_out_cargado(aristaNode,generation)
            arista.setNewProperties2(aristaNode.capacity,aristaNode.percentages[generation],aristaNode.amounts_of_cars[generation])
        elif aristaNode.typeArista == "normal": 
            arista = self.create_arista_normal_cargado(aristaNode,generation)
            arista.setNewProperties2(aristaNode.capacity,aristaNode.percentages[generation],aristaNode.amounts_of_cars[generation])
        
    
    def create_arista_normal_cargado(self,aristanormal,generation):
        circle1 = self.find_circle_by_name(aristanormal.circle1.name)
        circle2 = self.find_circle_by_name(aristanormal.circle2.name)
        arista = Arista(self.canvas, circle1, circle2)
        self.aristas.append(arista)
        circle1.aristasOut.append(arista)
        circle2.aristasIn.append(arista)
        return arista

    def create_arista_in_cargado(self,aristain,generation):
        circle2 = self.find_circle_by_name(aristain.circle2.name)
        arista_entrada = AristaIn(self.canvas, circle2)
        self.aristasIn.append(arista_entrada)
        circle2.aristasIn.append(arista_entrada)
        arista_entrada.circle1.aristasOut.append(arista_entrada)
        self.canvas.tag_bind(arista_entrada.circle1.shape, "<B1-Motion>", lambda event, circle=arista_entrada.circle1: circle.move(event))
        return arista_entrada

    def create_arista_out_cargado(self,aristaout,generation):
        circle1 = self.find_circle_by_name(aristaout.circle1.name)
        arista_salida = AristaOutput(self.canvas, circle1)
        self.aristasOut.append(arista_salida)
        circle1.aristasOut.append(arista_salida)
        arista_salida.circle2.aristasIn.append(arista_salida)
        self.canvas.tag_bind(arista_salida.circle2.shape, "<B1-Motion>", lambda event, circle=arista_salida.circle2: circle.move(event))
        return arista_salida

    
    def find_circle_by_name(self,name):
        for circle in self.circles:
            if circle.name == name:
                return circle
        return None
        
    
    def crear_nodo_cargado(self,node):
        if isinstance(node,NodeModel):
            self.nameNode += 1
            circle = Circle(self.canvas, node.x, node.y, "white",str(node.name))
            self.circles.append(circle)
            self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
            self.canvas.tag_bind(circle.shape, "<B1-Motion>", lambda event, circle=circle: circle.move(event))
            self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event: self.borrar_nodo_seleccionado(event))
                
    
    def createDialogLoadModel(self):
        filename = filedialog.askopenfilename(filetypes=[("Model Files", "*.mdl")])
        if filename:
            self.loadModel(filename)


    def iniciar(self):
        menu_bar = tk.Menu(self.root)

        nodos_menu = tk.Menu(menu_bar, tearoff=0)
        nodos_menu.add_command(label="Crear Nodo", command=self.crear_nodo)
        nodos_menu.add_command(label="Borrar Nodo", command=self.toggle_borrado_nodo)
        menu_bar.add_cascade(label="Nodos", menu=nodos_menu)

        aristas_menu = tk.Menu(menu_bar, tearoff=0)
        aristas_menu.add_command(label="Crear Arista", command=self.toggle_creacion_arista)
        aristas_menu.add_command(label="Crear Arista Salida", command=self.toggle_creacion_arista_salida)
        aristas_menu.add_command(label="Crear Arista Entrada", command=self.toggle_creacion_arista_entrada)
        aristas_menu.add_command(label="Borrar Arista", command=self.borrar_arista)
        aristas_menu.add_command(label="Actualizar Arista", command=self.toggle_actualizando_arista)
        menu_bar.add_cascade(label="Aristas", menu=aristas_menu)

        model_menu = tk.Menu(menu_bar, tearoff=0)
        model_menu.add_command(label="Ingresar Datos", command=self.saveDataFromModel)
        model_menu.add_command(label="Iniciar Modelo", command=self.initModel)
        model_menu.add_command(label="Cargar Modelo", command=self.createDialogLoadModel)
        menu_bar.add_cascade(label="Modelo", menu=model_menu)

        canvas_menu = tk.Menu(menu_bar, tearoff=0)
        canvas_menu.add_command(label="Limpiar Canvas", command=self.cleanCanvas)
        menu_bar.add_cascade(label="Tablero", menu=canvas_menu)

        self.root.config(menu=menu_bar)

        self.canvas.bind("<Button-1>", self.borrar_arista_seleccionada)

        self.root.mainloop()

if __name__ == "__main__":
    app = Interfaz()
    app.iniciar()
