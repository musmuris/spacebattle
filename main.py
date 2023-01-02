import pyglet
from pyglet.window import key

PLAYER_SPEED = 300.0

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
player = pyglet.sprite.Sprite(img=player_image, x=window.width/2, y=player_image.height)


@window.event
def on_draw():
    window.clear()
    player.draw()

def update(dt):
    if keys[key.LEFT] and player.x > player.width / 2 + 10:
            player.x -= dt * PLAYER_SPEED
    if keys[key.RIGHT] and player.x < window.width - player.width / 2 - 10:
            player.x += dt * PLAYER_SPEED


pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()

