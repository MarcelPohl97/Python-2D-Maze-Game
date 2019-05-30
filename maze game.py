from tkinter import *
import random
import time
game_window = Tk()
game_root = Canvas(game_window, width=1280, height=832, bg="green")
game_root.pack()

move_left = PhotoImage(file="right.gif")
move_right = PhotoImage(file="left.gif")
jump_ = PhotoImage(file="jump.gif")
stop_ = PhotoImage(file="stop.gif")

move_left_enemy = PhotoImage(file="right_enemy.gif")
move_right_enemy = PhotoImage(file="left_enemy.gif")
jump_enemy = PhotoImage(file="jump_enemy.gif")
stop_enemy = PhotoImage(file="stop_enemy.gif")

colors = ["#abef4c", "#69dff4", "#bc85f7", "#ff72aa", "#fc3a3a", "#3aaefc", "#ffc711", "#f47b11", "#f43a11"]


class Player:
    def __init__(self):
        self.player_id = game_root.create_image(32, 32, image=move_left)
        self.Left = False
        self.Right = False
        self.Up = False
        self.Down = False
        self.jump = -16
        self.speed = 16
        self.player_update()

    def move_direction(self, event):
        key = event.keysym
        if key == 'd':
            self.Right = True

        if key == "a":
            self.Left = True

        if key == "w":
            self.Up = True

        if key == "s":
            self.Down = True

    def stop_direction(self, event):
        key = event.keysym
        if key == 'a':
            self.Left = False

        if key == 'd':
            self.Right = False

        if key == 'w':
            self.Up = False

        if key == "s":
            self.Down = False

    def player_update(self):
        if self.Left:
            game_root.itemconfig(self.player_id, image=move_right)
            game_root.move(self.player_id, -self.speed, 0)

        if self.Right:
            game_root.itemconfig(self.player_id, image=move_left)
            game_root.move(self.player_id, self.speed, 0)

        if self.Up:
            game_root.itemconfig(self.player_id, image=jump_)
            game_root.move(self.player_id, 0, self.jump)

        if self.Down:
            game_root.move(self.player_id, 0, -self.jump)

        if not (self.Left or self.Right or self.Up or self.Down):
            game_root.itemconfig(self.player_id, image=stop_)

        game_root.after(100, self.player_update)


class Map:
    def __init__(self, x, y, color, enemy_list):
        self.map_id = game_root.create_rectangle(64, 64, 0, 0, fill=color)
        self.enemy_list = enemy_list
        game_root.move(self.map_id, x, y)

    def player_collision_x(self):
        x1, y1, x2, y2 = game_root.coords(self.map_id)
        collision = game_root.find_overlapping(x1, y1, x2, y2)
        
        if S.Right == True and S.player_id in collision:
            game_root.move(S.player_id, -S.speed, 0)

        if S.Left == True and S.player_id in collision:
            game_root.move(S.player_id, S.speed, 0)

        game_root.after(100, self.player_collision_x)

    def player_collision_y(self):
        x1, y1, x2, y2 = game_root.coords(self.map_id)
        collision = game_root.find_overlapping(x1, y1, x2, y2)
        
        if S.Up == True and S.player_id in collision:
            game_root.move(S.player_id, 0, - S.jump)

        if S.Down == True and S.player_id in collision:
            game_root.move(S.player_id, 0, S.jump)

        game_root.after(100, self.player_collision_y)

    def enemy_collision_y(self):
        x1, y1, x2, y2 = game_root.coords(self.map_id)
        collision = game_root.find_overlapping(x1, y1, x2, y2)
        for enemys in enemy_list:
            if enemys.enemy_id in collision and enemys.dir == "up":
                game_root.move(enemys.enemy_id, 0, 16)
                enemys.dir = random.choice(["up", "down", "left", "right"])

            if enemys.enemy_id in collision and enemys.dir == "down":
                game_root.move(enemys.enemy_id, 0, -16)
                enemys.dir = random.choice(["up", "down", "left", "right"])

        game_root.after(100, self.enemy_collision_y)

    def enemy_collision_x(self):
        x1, y1, x2, y2 = game_root.coords(self.map_id)
        collision = game_root.find_overlapping(x1, y1, x2, y2)
        for enemys in enemy_list:

            if enemys.enemy_id in collision and enemys.dir == "left":
                game_root.move(enemys.enemy_id, 16, 0)
                enemys.dir = random.choice(["up", "down", "left", "right"])

            if enemys.enemy_id in collision and enemys.dir == "right":
                game_root.move(enemys.enemy_id, -16, 0)
                enemys.dir = random.choice(["up", "down", "left", "right"])

        game_root.after(100, self.enemy_collision_x)


class Enemy:
    def __init__(self, x, y):
        self.enemy_id = game_root.create_image(32, 32, image=stop_enemy)
        game_root.move(self.enemy_id, x, y)
        self.dir = random.choice(["up", "down", "left", "right"])
        self.enemy_update()
    def enemy_update(self):

        if self.dir == "up":
            self.speed = 0
            self.jump = -16
        elif self.dir == "down":

            self.speed = 0
            self.jump = 16
        elif self.dir == "left":

            self.speed = -16
            self.jump = 0
        elif self.dir == "right":

            self.speed = 16
            self.jump = 0
        else:
            self.speed = 0
            self.jump = 0
            
        game_root.move(self.enemy_id, self.speed, self.jump)
        game_root.after(100, self.enemy_update)

levels = []

level_1 = ["####################",
           "#P#       #  E     #",
           "#   ## # ## #### # #",
           "# #  E # #  #  E  ##",
           "# # ## #        #  #",
           "# #    # ## #      #",
           "#  # #    # # ## # #",
           "#    #  #   # # #  #",
           "# ## #   # E  # #  #",
           "#  E #  #   #      #",
           "# ##  #     # ### ##",
           "#         E   #    #",
           "####################"]

levels.append(level_1)

def setup_maze(level):
    global map_list, enemy_list, screen_x, screen_y
    map_list = []
    enemy_list = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            sprite = level[y][x]
            screen_x = 0 + (x * 64)
            screen_y = 0 + (y * 64)

            if sprite == "#":
                map_list.append(Map(screen_x, screen_y, random.choice(colors), enemy_list))

            if sprite == "P":
                game_root.move(S.player_id, screen_x, screen_y)

            if sprite == "E":
                enemy_list.append(Enemy(screen_x, screen_y))

S = Player()

setup_maze(levels[0])

for enemy in enemy_list:
    enemy.enemy_update()

for map in map_list:
    map.player_collision_x()
    map.player_collision_y()
    map.enemy_collision_y()
    map.enemy_collision_x()

game_window.bind("<KeyPress>",S.move_direction)
game_window.bind("<KeyRelease>", S.stop_direction)
game_window.mainloop()
