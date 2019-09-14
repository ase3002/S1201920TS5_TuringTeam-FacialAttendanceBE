from django.urls import path
from .views import post_attendace_img, index

urlpatterns = [
    path('', index, name='index'),
    path('image/', post_attendace_img)
]
