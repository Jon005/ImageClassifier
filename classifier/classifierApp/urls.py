from django.contrib import admin
from django.urls import path
from .views import home,predictImage,viewDataBase
urlpatterns = [
    path('',home,name='home'),
    path('predictImage',predictImage,name='predictImage'),
    path('viewDataBase',viewDataBase,name='viewDataBase')
]
