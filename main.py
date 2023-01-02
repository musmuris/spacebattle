import pyglet
from pyglet.window import key
import images
import random
import sys

# Images from Kenney at https://www.kenney.nl/assets/space-shooter-redux

PLAYER_SPEED = 300.0
LASER_SPEED = 500.0
LASER_COOLDOWN = 0.5
ENEMY_SPEED = 500.0
ENEMY_COOLDOWN = 1.0


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
state.lastEnemyTime = 0
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


background = pyglet.image.TileableTexture.create_for_image(images.black_background)

player = pyglet.sprite.Sprite(img=player_image, x=window.width // 2, y=player_image.height)
player.bounds = Bounds(player)
player.name = "player"

lasers = []
laserbatch = pyglet.graphics.Batch()

enemies = []
enemybatch = pyglet.graphics.Batch()

def shoot():
    laser = pyglet.sprite.Sprite(img=laser_image, x=player.x, y=player.y+10, batch=laserbatch)
    laser.bounds = Bounds(laser)
    laser.name = "laser"
    lasers.append(laser)

def spawnEnemy():
    xpoint = random.random() * (window.width/2) + window.width/4
    enemy = pyglet.sprite.Sprite(img=enemy_image, x=xpoint // 1, y=window.height + enemy_image.height, batch=enemybatch)
    enemy.scale = 0.5
    enemy.xdir = 1 if random.random() > 0.5 else -1
    enemy.bounds = Bounds(enemy)
    enemy.name = "enemy"
    enemies.append(enemy)

def updateLasers(dt):
    deadlaser = []
    for laser in lasers: 
        laser.y += dt * LASER_SPEED
        if laser.y > window.height + laser_image.height:
            deadlaser.append(laser)

    for laser in deadlaser:
        laser.delete()
        lasers.remove(laser)

def updateEnemies(dt):
    if state.timeSoFar - state.lastEnemyTime > ENEMY_COOLDOWN:
        state.lastEnemyTime = state.timeSoFar
        spawnEnemy()

    deadenemies = []
    for enemy in enemies:
        enemy.y -= dt * 200
        enemy.x += dt * 200 * enemy.xdir
        if enemy.x > window.width - 30 or enemy.x < 30:
            enemy.xdir = -enemy.xdir
        if enemy.y < -enemy.height:
            deadenemies.append(enemy)
    
    for enemy in deadenemies:
        enemy.delete()
        enemies.remove(enemy)               

def collisions():
    deadlaser = []
    deadenemies = []
    for enemy in enemies:
        if enemy.bounds.collides_with(player.bounds):
            sys.exit(0)            
        for laser in lasers:
            if laser.bounds.collides_with(enemy.bounds):        
                deadenemies.append(enemy)
                deadlaser.append(laser)
                state.score += 1
    for laser in deadlaser:
        laser.delete()                
        lasers.remove(laser)
    for enemy in deadenemies:
        enemy.delete()
        enemies.remove(enemy)               

def update(dt):
    state.timeSoFar += dt

    collisions()

    updateLasers(dt)

    updateEnemies(dt)

    if keys[key.LEFT] and player.x > player.width // 2 + 10:
            player.x -= dt * PLAYER_SPEED
    if keys[key.RIGHT] and player.x < window.width - player.width // 2 - 10:
            player.x += dt * PLAYER_SPEED
    if keys[key.SPACE] and (state.timeSoFar - state.lastLaserTime) > LASER_COOLDOWN:
        state.lastLaserTime = state.timeSoFar
        shoot()

@window.event
def on_draw():
    window.clear()
    background.blit_tiled(0, 0, 0, window.width, window.height)
    laserbatch.draw()
    enemybatch.draw()
    player.draw()
    
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

