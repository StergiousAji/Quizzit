from django.urls import path
from quizzit_app import views

app_name = 'quizzit'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('howtoplay/', views.howtoplay,name='howtoplay'),
]