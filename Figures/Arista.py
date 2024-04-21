import tkinter as tk
class Arista:
    def __init__(self, canvas, circle1, circle2, color="black"):
        self.canvas = canvas
        self.circle1 = circle1
        self.circle2 = circle2
        self.calculate_arrow_coordinates()
        self.arrow = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, arrow=tk.LAST, fill=color)

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

    def actualizar(self):
        self.calculate_arrow_coordinates()
        self.canvas.coords(self.arrow, self.start_x, self.start_y, self.end_x, self.end_y)
