"""
URL configuration for UrbanDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task1.views import  Sign_user, Store_index, Store_sale, Store_basket,Game_Insert


urlpatterns = [
    path('game_store/signUser/', Sign_user.as_view()),
    path('game_store/', Store_index.as_view()),
    path('game_store/sale/', Store_sale.as_view()),
    path('game_store/basket/', Store_basket.as_view()),
    path('game_store/game_insert/', Game_Insert.as_view()),
]
