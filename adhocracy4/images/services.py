from easy_thumbnails.files import get_thumbnailer


def delete_images(imagefields):
    for imagefield in imagefields:
        if not imagefield: continue
        thumbnailer = get_thumbnailer(imagefield)
        thumbnailer.delete_thumbnails()
        if imagefield.name:
            imagefield.storage.delete(imagefield.name)
