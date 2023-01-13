import pyglet

class Actor(pyglet.sprite.Sprite):
    def __init__(self, img, x=0, y=0, batch=None, **kwargs):
        super(Actor, self).__init__(img, x=x, y=y, batch=batch, **kwargs)
        self.anchor_x = img.anchor_x
        self.anchor_y = img.anchor_y
        self.dead = False
 
    @property
    def top(self):
        return self.bottom + self.height
    
    @property
    def bottom(self):
        return self.y - self.anchor_y * self.scale

    @property
    def left(self):
        return self.x - self.anchor_x * self.scale

    @property
    def right(self):
        return self.left + self.width

    def collides_with(self, other):
        return (self.right >= other.left and
                self.left <= other.right and
                self.top >= other.bottom and
                self.bottom <= other.top )
