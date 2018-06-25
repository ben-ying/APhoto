from django.conf.urls import url
from django.urls import path

from .views import PhotoListView


app_name = 'ezphoto'
urlpatterns = [
    path('photos', PhotoListView.as_view(), name='photo-list'),
]
