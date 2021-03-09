from django.urls import path
from quizzit_app import views

app_name = 'quizzit'

urlpatterns = [
    path('', views.home, name='home'),
]