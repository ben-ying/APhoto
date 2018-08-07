import PIL.Image
import PIL.ExifTags

def readExif():
    img = PIL.Image.open('/home/ben/Pictures/IMG_5751.JPG')
    for k, v in img._getexif().items():
        if k in PIL.ExifTags.TAGS:
            print(PIL.ExifTags.TAGS[k] + ": " + str(v))
            if (isinstance(v, bytes)):
                print(v.decode("utf-8", "ignore"))
            print(type(v))
#            print(PIL.ExifTags.TAGS[k] + ": " + v)
    #exif = {
    #        PIL.ExifTags.TAGS[k]: v
    #        for k, v in img._getexif().items()
    #        if k in PIL.ExifTags.TAGS
    #        }
    #print(exif)
    # exif_data = img._getexif()
    #print("=====================================")
    #print(PIL.ExifTags.TAGS)

readExif()    
