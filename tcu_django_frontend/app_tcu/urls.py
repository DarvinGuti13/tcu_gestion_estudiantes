from django.urls import path
from . import views

urlpatterns = [
    path('solicitud/', views.solicitud_tcu_form, name='solicitud_tcu'),
    path('estado/', views.validar_estado, name='validar_estado'),

]
