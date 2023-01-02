import pyglet
from pyglet.window import key

PLAYER_SPEED = 300.0
LASER_SPEED = 500.0

window = pyglet.window.Window(1024,768)
keys = key.KeyStateHandler()
window.push_handlers(keys)

pyglet.resource.path = ['assets']
pyglet.resource.reindex()

def anchor_center_image(imageFile):
    image = pyglet.resource.image(imageFile)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

player_image = anchor_center_image("playerShip2_orange.png")
player = pyglet.sprite.Sprite(img=player_image, x=window.width // 2, y=player_image.height)

enemy_image = anchor_center_image("enemyBlue1.png")

laser_image = anchor_center_image("laserRed15.png")

lasers = []
laserbatch = pyglet.graphics.Batch()

enemies = []
enemybatch = pyglet.graphics.Batch()

def shoot():
    laser = pyglet.sprite.Sprite(img=laser_image, x=player.x, y=player.y+10, batch=laserbatch)
    lasers.append(laser)

def spawnEnemy():
    enemy = pyglet.sprite.Sprite(img=enemy_image, x=window.width // 2, y=700, batch=enemybatch)
    enemies.append(enemy)

@window.event
def on_draw():
    window.clear()
    laserbatch.draw()
    enemybatch.draw()
    player.draw()
    

LASER_COOLDOWN = 0.5
timeSoFar = 0
lastLaserTime = 0 

def update(dt):
    global timeSoFar, lastLaserTime

    timeSoFar += dt

    deadlaser = []
    for laser in lasers:
        laser.y += dt * LASER_SPEED
        if laser.y > window.height + laser_image.height:
            laser.delete()
            deadlaser.append(laser)
    for laser in deadlaser:
        lasers.remove(laser)

    if keys[key.LEFT] and player.x > player.width // 2 + 10:
            player.x -= dt * PLAYER_SPEED
    if keys[key.RIGHT] and player.x < window.width - player.width // 2 - 10:
            player.x += dt * PLAYER_SPEED
    if keys[key.SPACE] and (timeSoFar - lastLaserTime) > LASER_COOLDOWN:
        lastLaserTime = timeSoFar
        shoot()

    if len(enemies) == 0 :
        spawnEnemy()


pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

