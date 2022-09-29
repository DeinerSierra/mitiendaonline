from django.urls import path
from . import views
app_name = 'usuarios'
urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activar/<uidb64>/<token>/', views.activar, name='activar'),
]