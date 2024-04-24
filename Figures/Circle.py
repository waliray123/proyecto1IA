class Circle:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.shape = canvas.create_oval(x-20, y-20, x+20, y+20, fill=color)
        self.x = x
        self.y = y
        self.selected = False
        self.outline = ""
        self.aristasOut = []
        self.aristasIn = []

    def toggle_selection(self, event, selected_circles, creando_arista, borrando_arista):
        if creando_arista or borrando_arista:
            if len(selected_circles) == 2:
                selected_circles[-1].selected = False
                selected_circles[-1].outline = "black"
                selected_circles[-1].canvas.itemconfig(selected_circles[-1].shape, outline=selected_circles[-1].outline, width=1)
                selected_circles.pop()
            self.selected = not self.selected
            if borrando_arista:
                #borrar_arista_seleccionada(event)
                print("borrar arista")
            else:
                if self.selected:
                    if len(selected_circles) == 0:
                        self.outline = "blue"
                    else:
                        self.outline = "red"
                    selected_circles.append(self)
                else:
                    self.outline = "black"
                    selected_circles.remove(self)
                self.canvas.itemconfig(self.shape, outline=self.outline, width=3 if self.selected else 1)

    

    def move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.shape, dx, dy)
        self.x = event.x
        self.y = event.y
        for arista in self.aristasOut:
            arista.actualizar()
        for arista in self.aristasIn:
            arista.actualizar()