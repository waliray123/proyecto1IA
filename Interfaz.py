import tkinter as tk
from tkinter import messagebox

from Figures.Arista import Arista
from Figures.AristaOutput import AristaOutput
from Figures.AristaIn import AristaIn
from Figures.Circle import Circle
from Controllers.controlFigures import ControlFigures

class Interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplicación")
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.pack()
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
        self.label_estado = tk.Label(self.root, text="")
        self.label_estado.pack()
        self.boton_terminar_arista = tk.Button(self.root, text="Terminar Arista", command=self.crear_arista)
        self.boton_terminar_arista.pack_forget()
        self.controlFigures = ControlFigures()
        self.nameNode = 0

    def toggle_creacion_arista(self):
        self.creando_arista = not self.creando_arista
        if self.creando_arista:
            self.label_estado.config(text="Modo creación de arista activado. Seleccione dos nodos.")
            self.boton_terminar_arista.pack()
            for circle in self.circles:
                self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.pack_forget()
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
        self.boton_terminar_arista.pack_forget()

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
            self.boton_terminar_arista.pack_forget()
            for circle in self.circles:
                circle.selected = False
                circle.canvas.itemconfig(circle.shape, width=1)
            self.borrando_arista = True
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.pack_forget()
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
            self.boton_terminar_arista.pack_forget()
            self.borrando_nodo = True
        else:
            self.label_estado.config(text="")
            self.boton_terminar_arista.pack_forget()
            self.borrando_nodo = False

    def borrar_nodo_seleccionado(self, event):
        if self.borrando_nodo:
            circle_id = event.widget.find_closest(event.x, event.y)
            if circle_id and circle_id[0] in [circle.shape for circle in self.circles]:
                circle = next(circle for circle in self.circles if circle.shape == circle_id[0])
                self.circles.remove(circle)
                event.widget.delete(circle.shape)
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

    def initModel(self):
        self.controlFigures.validateAllFigures(self.aristas,self.circles)
        for exception in self.controlFigures.exceptions:
            print(exception.message)

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

        nodos_menu = tk.Menu(menu_bar, tearoff=0)
        nodos_menu.add_command(label="Iniciar Modelo", command=self.initModel)        
        menu_bar.add_cascade(label="Modelo", menu=nodos_menu)

        self.root.config(menu=menu_bar)

        self.canvas.bind("<Button-1>", self.borrar_arista_seleccionada)

        self.root.mainloop()

if __name__ == "__main__":
    app = Interfaz()
    app.iniciar()
