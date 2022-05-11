from PIL import Image

from .models import News


def make_thumb(path_to_image, size):
    try:
        new_image_path = add_prefix_to_file_name(path_to_image, News.THUMB_PREFIX)
        with Image.open(path_to_image) as im:
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(new_image_path, "JPEG")
        result = True
    except IOError:
        result = False
    return result


def add_prefix_to_file_name(path, prefix):
    arr = path.split('/')
    name = arr.pop()
    name = prefix + name
    arr.append(name)
    return '/' . join(arr)

