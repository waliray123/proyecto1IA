import tkinter as tk

from Figures.Circle import Circle
class AristaOutput:
    def __init__(self, canvas, circle1, color="black"):
        self.canvas = canvas
        self.circle1 = circle1        
        self.circle2 = Circle(self.canvas, circle1.x + 50, circle1.y, "red","Salida")
        self.canvas.tag_bind(self.circle2.shape, "<B1-Motion>", lambda event, circle=self.circle2: circle.move(event))
        self.capacity = 0
        self.percentage = 0
        self.start_x, self.start_y = circle1.x, circle1.y
        self.end_x, self.end_y = self.circle2.x, self.circle2.y         
        self.arrow = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, arrow=tk.LAST, fill=color)
        self.capacity_text = self.canvas.create_text((self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2, text=f"Capacidad: {self.capacity}", fill=color)
        self.percentage_text = self.canvas.create_text((self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2 + 15, text=f"Porcentaje: {self.percentage}%", fill=color)
        self.enviados = 0
        self.enviados_text = self.canvas.create_text((self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2 + 30, text=f"Enviados: {self.enviados}%", fill=color)
        self.calculate_arrow_coordinates()
        self.percentages = []
        self.amounts_of_cars = []

    def actualizar(self):
        self.calculate_arrow_coordinates()
        self.canvas.coords(self.arrow, self.start_x, self.start_y, self.end_x, self.end_y)
        self.canvas.coords(self.capacity_text, (self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2)
        self.canvas.coords(self.percentage_text, (self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2 + 15)
        self.canvas.coords(self.enviados_text, (self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2 + 30)

    def calculate_arrow_coordinates(self):
        x1, y1 = self.circle1.x, self.circle1.y
        x2, y2 = self.circle2.x, self.circle2.y
        r1 = 20
        r2 = 20
        d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if d == 0:
            self.start_x, self.start_y = x1, y1 + r1
            self.end_x, self.end_y = x2, y2 - r2
        else:
            self.start_x = x1 + (x2 - x1) * r1 / d
            self.start_y = y1 + (y2 - y1) * r1 / d
            self.end_x = x2 - (x2 - x1) * r2 / d
            self.end_y = y2 - (y2 - y1) * r2 / d
    
    def setNewProperties(self,capacity,percentage):
        self.capacity = int(capacity)
        self.percentage = int(percentage)       
        self.canvas.itemconfig(self.capacity_text, text=f"Capacidad: {self.capacity}")
        self.canvas.itemconfig(self.percentage_text, text=f"Porcentaje: {self.percentage}%")

    def setNewProperties2(self,capacity,percentage,enviados):
        self.capacity = int(capacity)
        self.percentage = int(percentage)
        self.enviados = int(enviados)
        self.canvas.itemconfig(self.capacity_text, text=f"Capacidad: {self.capacity}")
        self.canvas.itemconfig(self.percentage_text, text=f"Porcentaje: {self.percentage}%")
        self.canvas.itemconfig(self.enviados_text, text=f"Porcentaje: {self.enviados}%")
    
    def addNewPercentage(self,newPercentage):
        self.percentages.append(newPercentage)
    
    def addNewAmountOfCars(self,amount_of_cars):
        self.amounts_of_cars.append(amount_of_cars)

    def cleanArista(self):
        self.percentages = []
        self.amounts_of_cars = []
