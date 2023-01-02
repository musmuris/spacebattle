import pyglet

window = pyglet.window.Window(1024,768)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

pyglet.resource.path = ['assets']
pyglet.resource.reindex()

def anchor_center_image(imageFile):
    image = pyglet.resource.image(imageFile)
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
    return image

player_image = anchor_center_image("playerShip2_orange.png")
player_sprite = pyglet.sprite.Sprite(img=player_image, x=window.width/2, y=player_image.height)


@window.event
def on_draw():
    window.clear()
    player_sprite.draw()

pyglet.app.run()

