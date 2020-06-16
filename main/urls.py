# chat/urls.py
from django.urls import path
from . import views
from django.core.management import call_command

app_name = "main"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('kitchen/', views.kitchen, name='kitchen'),
    path('mealplan/', views.mealplan, name='mealplan'),
    path('account/', views.account, name='account'),
    path('recipes/', views.account, name='recipes'),
    path('timetable/', views.timetable, name='timetable'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('shopping_cart/', views.shopping_list, name='shopping_list'),
    path('<single_slug>', views.single_slug, name='single_slug'),
]