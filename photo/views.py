from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse

from .models import Photo
from .models import Picture

import os
import PIL.Image
import PIL.ExifTags
import hashlib


class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = 20

    
def detail(request):
    directory = "/home/ben/Pictures"

    if not os.path.isdir:
        return HttpResponse("Dir not exists")

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.lower().endswith("jpg") \
                    or filepath.lower().endswith("jpeg"): 
                saveImage(filepath)

    return HttpResponse("OK")

def saveImage(img_path):
    picture = Picture()
    hasher = hashlib.sha1()
    with open(img_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        picture.sha1sum = hasher.hexdigest()
    img = PIL.Image.open(img_path)

    for key_number, v in img._getexif().items():
        if key_number in PIL.ExifTags.TAGS:
            k = PIL.ExifTags.TAGS[key_number]
            print(k)
            if k == "ExifImageWidth":
                picture.exif_image_width = v
            if k == "ExifImageHeight":
                picture.exif_image_height = v
            if k == "Make":
                picture.exif_make = v
            if k == "Model":
                picture.exif_model = v
            if k == "LensMake":
                picture.exif_lens_make = v
            if k == "LensModel":
                picture.exif_lens_model = v
            if k == "ExifVersion":
                picture.exif_version = v
            if k == "SubjectLocation":
                picture.exif_subject_location = str(v)
            if k == "DateTime":
                datetime = v.split(" ")[0].replace(":", "-") \
                        + " " + v.split(" ")[1]
                picture.exif_datetime = datetime
            if k == "DateTimeOriginal":
                datetime_original = v.split(" ")[0].replace(":", "-") \
                        + " " + v.split(" ")[1]
                picture.exif_datetime_original = datetime_original
            if k == "DateTimeDigitized":
                datetime_digitized = v.split(" ")[0].replace(":", "-") \
                        + " " + v.split(" ")[1]
                picture.exif_datetime_digitized = datetime_digitized
        
    picture.save()
