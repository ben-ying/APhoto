from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import PhotoListView


app_name = 'ezphoto'
urlpatterns = [
    path('photos', PhotoListView.as_view(), name='photo-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
