from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='indexpage'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('mainpage/', views.mainPage, name='mainpage'),
    path('logout/', views.signout, name='signout'),
]