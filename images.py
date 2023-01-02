import xml.etree.ElementTree as xmltree
import pyglet

def load_images():

    def anchor_center_image(image):
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        return image

    class Images:
        pass

    pyglet.resource.path = ['assets']
    pyglet.resource.reindex()

    imageData = pyglet.resource.text("sheet.xml").text

    atlas = xmltree.fromstring(imageData)

    texture = pyglet.resource.image(atlas.attrib["imagePath"])

    images = Images()

    for child in atlas:
        if child.tag == "SubTexture" :
            x = int(child.attrib["x"])
            y = int(child.attrib["y"])            
            w = int(child.attrib["width"])
            h = int(child.attrib["height"])
            # Image data has origin at top, left. Pyglet uses bottom, left 
            y = texture.height - y - h
            setattr(images, child.attrib["name"].replace('.png', ''), anchor_center_image(texture.get_region(x=x,y=y,width=w,height=h)))

    return images