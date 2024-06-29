from django.contrib import admin

from django.contrib import admin
from .models import Pregunta , Respuesta ,Seccion

admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Seccion)
