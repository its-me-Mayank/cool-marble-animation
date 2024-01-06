
"""
Author: Mayank Sharma

Description:
This Python script utilizes Tkinter to create a visually appealing animation featuring
bouncing marbles on a canvas. The marbles exhibit dynamic movement, collisions, and a 
colorful display, providing an cool visual experience.
"""

import tkinter as tk
import random
import time

root = tk.Tk()
Frame_Width = 800
Frame_Height = 600
root.geometry(f"{Frame_Width}x{Frame_Height}")
root.title("Marbles")

canvas = tk.Canvas(root, width=Frame_Width, height=Frame_Height)
canvas.pack()
canvas.config(bg="black")


def dec2hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


canvas.create_oval(50, 50, 100, 100, fill=dec2hex(123, 48, 255), width=0)


class Marble:
    def __init__(self, canvas, size, color, x, y, stuck=False):
        self.canvas = canvas
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.dx = 6
        self.dy = 6
        self.stuck = stuck

    def draw(self):
        self.canvas.create_oval(self.x - self.size, self.y - self.size,
                                self.x + self.size, self.y + self.size, fill=self.color)

    def move(self):
        if not self.stuck:
            self.x += self.dx
            self.y += self.dy

    def bounce(self):
        if not self.stuck:
            if self.x - self.size < 0 or self.x + self.size > Frame_Width:
                self.dx *= -1
            if self.y - self.size < 0 or self.y + self.size > Frame_Height:
                self.dy *= -1


def create_multiple_marbles(num_marbles):
    marbles = []
    center_x = Frame_Width // 2
    center_y = Frame_Height // 2

    # Create one "stuck" marble (this one will be blue)
    marbles.append(Marble(canvas, 5, dec2hex(0, 0, 255),
                   center_x, center_y, stuck=True))

    for _ in range(num_marbles - 1):
        size = 5
        x = random.randint(size, Frame_Width - size)
        y = random.randint(size, Frame_Height - size)

        # Calculate color based on distance from the center (blue to red gradient)
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        max_distance = (Frame_Width**2 + Frame_Height**2)**0.5
        r = int(255 * (1 - distance / max_distance))
        g = 0
        b = int(255 * (distance / max_distance))

        color = dec2hex(r, g, b)

        marble = Marble(canvas, size, color, x, y)
        marbles.append(marble)
        marble.draw()

    return marbles


def check_collision_with_stuck_marble(marbles):
    for marble in marbles:
        if not marble.stuck:
            for stuck_marble in marbles:
                if stuck_marble.stuck:
                    distance = ((marble.x - stuck_marble.x) ** 2 +
                                (marble.y - stuck_marble.y) ** 2) ** 0.5
                    if distance <= marble.size + stuck_marble.size:
                        marble.stuck = True


def update_marbles(marbles):
    for marble in marbles:
        marble.move()
        marble.bounce()


def animate_marbles():
    num_marbles = 100
    marbles = create_multiple_marbles(num_marbles)

    while True:
        check_collision_with_stuck_marble(marbles)
        update_marbles(marbles)

        stuck_marbles = [marble for marble in marbles if marble.stuck]

        # Check if all marbles are stuck in the center
        if len(stuck_marbles) == num_marbles:
            # Create 10 more marbles in the center
            center_x = Frame_Width // 2
            center_y = Frame_Height // 2
            for _ in range(10):
                size = 5
                color = "cyan"
                x = center_x
                y = center_y
                marble = Marble(canvas, size, color, x, y)
                marbles.append(marble)
                marble.draw()

        canvas.delete("all")
        for marble in marbles:
            marble.draw()
        root.update()
        time.sleep(0.025)


animate_marbles()
root.mainloop()
