from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Photo


class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = 20
