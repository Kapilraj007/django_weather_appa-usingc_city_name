
from django.contrib import admin
from django.urls import path
from weatherApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.weather,name="Weather"),
    path('delete/<CName>',views.delete_city,name="DCity")
]
