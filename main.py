import pyglet
from pyglet.window import key
import images

# Images from Kenney at https://www.kenney.nl/assets/space-shooter-redux

PLAYER_SPEED = 300.0
LASER_SPEED = 500.0
LASER_COOLDOWN = 0.5

window = pyglet.window.Window(1024,768)
keys = key.KeyStateHandler()
window.push_handlers(keys)

images = images.load_images()

class State:
    pass

state = State()

player_image = images.playerShip2_orange
enemy_image = images.enemyBlue1
laser_image = images.laserRed15
state.timeSoFar = 0
state.lastLaserTime = 0
state.score = 0 


class Bounds:
    def __init__(self, sprite):
        self.sprite = sprite
    
    @property
    def top(self):
        return self.bottom + self.sprite.height
    
    @property
    def bottom(self):
        return self.sprite.y - self.sprite.image.anchor_y * self.sprite.scale

    @property
    def left(self):
        return self.sprite.x - self.sprite.image.anchor_x * self.sprite.scale

    @property
    def right(self):
        return self.left + self.sprite.width

    def collides_with(self, other):
        return (self.right >= other.left and
                self.left <= other.right and
                self.top >= other.bottom and
                self.bottom <= other.top )


player = pyglet.sprite.Sprite(img=player_image, x=window.width // 2, y=player_image.height)
player.bounds = Bounds(player)

lasers = []
laserbatch = pyglet.graphics.Batch()

enemies = []
enemybatch = pyglet.graphics.Batch()

def shoot():
    laser = pyglet.sprite.Sprite(img=laser_image, x=player.x, y=player.y+10, batch=laserbatch)
    laser.bounds = Bounds(laser)
    lasers.append(laser)

def spawnEnemy():
    enemy = pyglet.sprite.Sprite(img=enemy_image, x=window.width // 2, y=700, batch=enemybatch)
    enemy.scale = 0.5
    enemy.bounds = Bounds(enemy)
    enemies.append(enemy)

def updateLasers(dt):
    deadlaser = []
    for laser in lasers: 
        laser.y += dt * LASER_SPEED
        if laser.y > window.height + laser_image.height:
            laser.delete()
            deadlaser.append(laser)
    for laser in deadlaser:
        lasers.remove(laser)

def collisions():
    deadlaser = []
    deadenemies = []
    for enemy in enemies:
        for laser in lasers:
            if laser.bounds.collides_with(enemy.bounds):        
                laser.delete()
                enemy.delete()
                deadlaser.append(laser)
                state.score += 1
    for laser in deadlaser:
        lasers.remove(laser)
    for enemy in deadenemies:
        enemy.remove(laser)               

def update(dt):
    state.timeSoFar += dt

    collisions()

    updateLasers(dt)

    if keys[key.LEFT] and player.x > player.width // 2 + 10:
            player.x -= dt * PLAYER_SPEED
    if keys[key.RIGHT] and player.x < window.width - player.width // 2 - 10:
            player.x += dt * PLAYER_SPEED
    if keys[key.SPACE] and (state.timeSoFar - state.lastLaserTime) > LASER_COOLDOWN:
        state.lastLaserTime = state.timeSoFar
        shoot()

    if len(enemies) == 0 :
        spawnEnemy()

@window.event
def on_draw():
    window.clear()
    laserbatch.draw()
    enemybatch.draw()
    player.draw()
    
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

