import tkinter as tk

class Game(tk.Frame):
    flg=1
    flg2=1
    flg3=1
    flg4=1
    flg5=1
    flg6=1

    def __init__(self, master):
        super(Game, self).__init__(master)
        self.width = 610
        self.height= 400
        self.canvas = tk.Canvas(self, bg = '#aaaaaa', width = self.width, height = self.height)
        self.canvas.pack()
        self.pack()
        self.ball = Ball(self.canvas, self.width/2, 310)

        self.items = {}
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle
        self.brick = Brick(self.canvas, self.width /1.3,10, 1)
        self.items[self.brick.item] = self.brick
        self.brick2 = Brick2(self.canvas, self.width / 1.1, 10, 1)
        self.items[self.brick2.item] = self.brick2
        self.brick3 = Brick3(self.canvas, self.width /1.5, 10, 1)
        self.items[self.brick3.item] = self.brick3
        self.brick4 = Brick4(self.canvas, self.width / 1.7, 10, 1)
        self.items[self.brick4.item] = self.brick4
        self.brick5 = Brick5(self.canvas, self.width /1.9, 10, 1)
        self.items[self.brick5.item] = self.brick5
        self.brick6 = Brick6(self.canvas, self.width / 2.3, 10, 1)
        self.items[self.brick6.item] = self.brick6

        self.game_loop()
        self.canvas.focus_set()
        self.canvas.bind('<Up>',
                         lambda _: self.ball.switch())

    def game_loop(self):
        self.check_collisions()
        self.ball.update()
        if Game.flg ==1:
            self.brick.update()
        if Game.flg2 ==1:
            self.brick2.update()
        if Game.flg3 ==1:
            self.brick3.update()
        if Game.flg4 ==1:
            self.brick4.update()
        if Game.flg5 ==1:
            self.brick5.update()
        if Game.flg6 ==1:
            self.brick6.update()

        self.after(30, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

class GameObject:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 10
        self.height = 20
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='orange')
        super(Paddle, self).__init__(canvas, item)

    def move(self, velocity):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + velocity >= 0 and coords[2] + velocity <= width: #coords == [x1, y1, x2, y2]
            super(Paddle, self).move(velocity, 0)

class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 5
        self.direction = [0, -1]
        self.speed = 0
        self.Switch = False
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

    def Newball(self, canvas, x, y):
        self.radius = 5
        self.direction = [0, -1]
        self.speed = 0
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

    def switch(self):
           self.Switch +=1 #~self.Switch

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[1] <= -20:
            self.direction[1] = 0
            self.delete()
            self.Newball(self.canvas, 610 / 2, 310)
            self.Switch = False

        if self.Switch == False:
            self.speed = 0

        else:
            self.speed = 10

        y = self.direction[1] * self.speed
        self.move(0.0, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= 1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            self.delete()
            self.Newball(self.canvas, 610/2, 310)

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()
                self.Switch = False
        for game_object in game_objects:
            if isinstance(game_object, Brick2):
                game_object.hit()
                self.Switch = False
        for game_object in game_objects:
            if isinstance(game_object, Brick3):
                game_object.hit()
                self.Switch = False

        for game_object in game_objects:
            if isinstance(game_object, Brick4):
                game_object.hit()
                self.Switch = False

        for game_object in game_objects:
            if isinstance(game_object, Brick5):
                game_object.hit()
                self.Switch = False
        for game_object in game_objects:
            if isinstance(game_object, Brick6):
                game_object.hit()
                self.Switch = False

class Brick(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'green'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg=Game.flg - 1
            self.delete()

class Brick2(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'red'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick2, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg2=Game.flg2 - 1
            self.delete()

class Brick3(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'blue'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick3, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg3=Game.flg3 - 1
            self.delete()

class Brick4(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'black'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick4, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg4=Game.flg4 - 1
            self.delete()

class Brick5(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'yellow'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick5, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg5=Game.flg5 - 1
            self.delete()

class Brick6(GameObject):
    def __init__(self, canvas, x, y, hits):
        self.width = 50
        self.height = 20
        self.direction = [1,0]
        self.speed = 10
        self.hits = 1
        color = 'purple'
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick6, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        x = self.direction[0] * self.speed
        self.move(x, 0)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            Game.flg6=Game.flg6 - 1
            self.delete()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Game Title')
    game = Game(root)
    game.mainloop()

