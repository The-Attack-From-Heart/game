import math
import random
import arcade

SPRITE_SPEED = 2


class Kristian(arcade.Sprite):

    def follow(self, target):
        if self.center_y < target.center_y:
            self.center_y += min(SPRITE_SPEED, target.center_y - self.center_y)
        elif self.center_y > target.center_y:
            self.center_y -= min(SPRITE_SPEED, self.center_y - target.center_y)

        if self.center_x < target.center_x:
            self.center_x += min(SPRITE_SPEED, target.center_x - self.center_x)
        elif self.center_x > target.center_x:
            self.center_x -= min(SPRITE_SPEED, self.center_x - target.center_x)
 

class Game(arcade.Window):
    def __init__(self):
        super().__init__(1536, 800, "You get lost", resizable=True)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # List of enemies
        self.enemy = arcade.Sprite("resources/textures/enemy_250_2.png", scale=1.25)
        self.player = arcade.Sprite("resources/textures/player.jpg", scale=0.1)
        self.enemy_list = arcade.SpriteList()
        # Router target
        self.tm = arcade.Sprite("resources/textures/router-raw.png", scale=0.25)
        self.spawn_timer = 0
        self.spawn_time = 1
        self.num_spawns = 0
        self.update_center()
        self.game_over = False

    def update_center(self):
        self.center_x, self.center_y = self.get_framebuffer_size()
        self.center_x //= 2
        self.center_y //= 2
        self.tm.position = self.center_x, self.center_y
        self.enemy.position = self.center_x, self.center_y

    def on_draw(self):
        """ Render the screen. """
        self.clear()

        if self.game_over:
            self.enemy.draw()
            arcade.draw_text("NO MORE INTERNET!", self.center_x - 400, self.center_y * 1.5, (255, 0, 0), 76)
        else:
            self.update_center()
            self.tm.draw()
            self.enemy_list.draw()
            self.player.draw()
            arcade.draw_text(str(self.num_spawns), 20, 50, (0, 0, 0), 32)

    def on_update(self, dt):
        self.spawn_timer += dt

        if self.game_over:
            return

        # Spawn mechanics
        if self.spawn_timer >= self.spawn_time:
            # Spawn
            enemy = Kristian("resources/textures/enemy_250_2.png", scale=0.25)
            rnd_angle = random.random() * math.pi * 2
            enemy.position = (
                self.center_x + math.sin(rnd_angle) * 700,
                self.center_y + math.cos(rnd_angle) * 700,
            )
            self.enemy_list.append(enemy)
            self.spawn_timer = 0
            self.num_spawns += 1
            self.spawn_time *= 0.98

        # Move enemies
        for enemy in self.enemy_list:
            enemy.follow(self.tm)
    
        # Detect picking up enemies
        for sprite in self.player.collides_with_list(self.enemy_list):
            self.enemy_list.remove(sprite)

        # Detect enemy reaching goal
        if self.tm.collides_with_list(self.enemy_list):
            self.game_over = True

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.player.position = x, y

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.update_center()


window = Game()
arcade.run()

