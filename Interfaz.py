import tkinter as tk

from Figures.Arista import Arista
from Figures.Circle import Circle
class Interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplicación")
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.pack()
        self.circles = []
        self.aristas = []
        self.selected_circles = []
        self.creando_arista = False
        self.borrando_arista = False
        self.label_estado = tk.Label(self.root, text="")
        self.label_estado.pack()
        self.boton_terminar_arista = tk.Button(self.root, text="Terminar Arista", command=self.crear_arista)
        self.boton_terminar_arista.pack()

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
        circle1.aristas.append(arista)
        circle2.aristas.append(arista)
        self.selected_circles.clear()
        for circle in self.circles:
            circle.selected = False
            circle.canvas.itemconfig(circle.shape, outline="black", width=1)
        self.creando_arista = False
        self.label_estado.config(text="Creación de arista finalizada.")
        self.boton_terminar_arista.pack_forget()

    def crear_nodo(self):
        circle = Circle(self.canvas, 50, 50, "white")
        self.circles.append(circle)
        self.canvas.tag_bind(circle.shape, "<Button-1>", lambda event, circle=circle: circle.toggle_selection(event, self.selected_circles, self.creando_arista, self.borrando_arista))
        self.canvas.tag_bind(circle.shape, "<B1-Motion>", lambda event, circle=circle: circle.move(event))

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
            if arista_id and arista_id[0] in [arista.arrow for arista in self.aristas]:
                arista = next(arista for arista in self.aristas if arista.arrow == arista_id[0])
                self.aristas.remove(arista)
                event.widget.delete(arista.arrow)
                for circle in self.circles:
                    if arista in circle.aristas:
                        circle.aristas.remove(arista)
                self.label_estado.config(text="Arista borrada. Modo borrado de arista desactivado.")
                self.borrando_arista = False

    def iniciar(self):
        menu_bar = tk.Menu(self.root)

        nodos_menu = tk.Menu(menu_bar, tearoff=0)
        nodos_menu.add_command(label="Crear Nodo", command=self.crear_nodo)
        menu_bar.add_cascade(label="Nodos", menu=nodos_menu)

        aristas_menu = tk.Menu(menu_bar, tearoff=0)
        aristas_menu.add_command(label="Crear Arista", command=self.toggle_creacion_arista)
        aristas_menu.add_command(label="Borrar Arista", command=self.borrar_arista)
        menu_bar.add_cascade(label="Aristas", menu=aristas_menu)

        self.root.config(menu=menu_bar)

        self.canvas.bind("<Button-1>", self.borrar_arista_seleccionada)

        self.root.mainloop()

if __name__ == "__main__":
    app = Interfaz()
    app.iniciar()
