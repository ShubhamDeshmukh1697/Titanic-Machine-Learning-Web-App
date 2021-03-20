from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('result/', views.result,name="result"),
    path('search/', views.search,name="search"),
    path('predictions/', views.predictions,name="predictions"),

]

