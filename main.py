import pyglet
from pyglet.window import key
from actor import Actor
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

enemy_image = images.enemyBlue1
laser_image = images.laserRed15
state.timeSoFar = 0
state.lastLaserTime = 0
state.lastEnemyTime = 0
state.score = 0 

class Player(Actor):
    def __init__(self, batch, **kwargs):
        image = images.playerShip2_orange
        super(Player, self).__init__(img=image, x=window.width // 2, y=image.height, batch=batch, **kwargs)
        self.name = "player"

class Laser(Actor):
    def __init__(self, **kwargs):
        super(Laser,self).__init__(img=images.laserRed15, **kwargs)

    def update(self,dt):
        self.y += dt * LASER_SPEED
        if self.y > window.height + laser_image.height:
            self.dead = True

class Enemy(Actor):
    def __init__(self, **kwargs):
        super(Enemy,self).__init__(img=images.enemyBlue1, **kwargs)
        self.scale = 0.5
        self.xdir = 1 if random.random() > 0.5 else -1
        self.name = "enemy"

    def update(self,dt):
        self.y -= dt * 200
        self.x += dt * 200 * self.xdir
        if self.x > window.width - 30 or self.x < 30:
            self.xdir = -self.xdir
        if self.y < -self.height:
            self.dead = True
    

background = pyglet.image.TileableTexture.create_for_image(images.black_background)

playerbatch = pyglet.graphics.Batch()
player = Player(batch=playerbatch)

lasers = []
laserbatch = pyglet.graphics.Batch()

enemies = []
enemybatch = pyglet.graphics.Batch()

def shoot():
    laser = Laser(x=player.x, y=player.y+10, batch=laserbatch)
    lasers.append(laser)

def spawnEnemy():
    xpoint = random.random() * (window.width/2) + window.width/4
    enemy = Enemy(x=xpoint // 1, y=window.height + enemy_image.height, batch=enemybatch)
    enemies.append(enemy)

def updateLasers(dt):
    for laser in lasers:
        laser.update(dt)

def updateEnemies(dt):
    if state.timeSoFar - state.lastEnemyTime > ENEMY_COOLDOWN:
        state.lastEnemyTime = state.timeSoFar
        spawnEnemy()

    for enemy in enemies:
        enemy.update(dt)
    
def collisions():
    for enemy in enemies:
        if enemy.collides_with(player):
            player.dead = True            
        for laser in lasers:
            if laser.collides_with(enemy):        
                enemy.dead = True
                laser.dead = True
                state.score += 1

def removeDead(actors):
    dead = []
    for actor in actors:
        if actor.dead:
            actor.delete()
            dead.append(actor)
    for actor in dead:
        actors.remove(actor)               

def update(dt):
    state.timeSoFar += dt

    if player.dead:
        sys.exit(0)
        
    collisions()

    updateLasers(dt)

    updateEnemies(dt)

    removeDead(lasers)
    removeDead(enemies)

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
    background.blit_tiled(0, 0, 0, window.width, window.height )
    laserbatch.draw()
    enemybatch.draw()
    player.draw()
    
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

