from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .models import Photo
from .models import Picture
from myproject.settings import MEDIA_ROOT
from myproject.settings import BIRTHDAY

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
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.lower().endswith("jpg") \
                    or file_path.lower().endswith("jpeg"): 
                saveImage(file_path, file_name)

    return HttpResponse("OK")

def saveImage(file_path, file_name):
    picture = Picture()
    picture.name = file_name
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        picture.sha1sum = hasher.hexdigest()

    if not Picture.objects.filter(sha1sum = picture.sha1sum):
        img = PIL.Image.open(file_path)
        for key_number, v in img._getexif().items():
            if key_number in PIL.ExifTags.TAGS:
                k = PIL.ExifTags.TAGS[key_number]
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
                    moveImage(file_name, file_path, datetime)
                if k == "DateTimeOriginal":
                    datetime_original = v.split(" ")[0].replace(":", "-") \
                            + " " + v.split(" ")[1]
                    picture.exif_datetime_original = datetime_original
                if k == "DateTimeDigitized":
                    datetime_digitized = v.split(" ")[0].replace(":", "-") \
                            + " " + v.split(" ")[1]
                    picture.exif_datetime_digitized = datetime_digitized
        
        picture.save()


def moveImage(file_name, file_path, img_datetime):
    photo_dir = os.path.join(MEDIA_ROOT, "photo")
    delta = relativedelta(datetime.strptime(
        img_datetime.split(" ")[0], '%Y-%m-%d'), 
        datetime.strptime(BIRTHDAY, '%Y-%m-%d'))

    if delta.years == 0:
        img_dir = os.path.join(photo_dir, str(delta.months + 1) + "M")
    else:
        img_dir = os.path.join(photo_dir, str(delta.years + 1) + "Y")

    os.makedirs(img_dir, exist_ok=True)
    os.rename(file_path, os.path.join(img_dir, file_name))
