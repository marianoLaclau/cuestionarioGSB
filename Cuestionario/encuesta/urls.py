# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('datos/',views.principal,name='principal'),
    path('home/', views.home, name='home'),
    path('seccion/<int:seccion_id>/pregunta/<int:pregunta_id>/', views.renderizar_pregunta, name='renderizar_pregunta'),
    path('seccion/<int:seccion_id>/procesar/', views.procesar_respuesta, name='procesar_respuesta'),
    path('final/', views.final_cuestionario, name='final_cuestionario'),
    path('', views.enviar_email, name='finalizar_cuestionario')
]



