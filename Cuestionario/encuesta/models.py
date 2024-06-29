from django.db import models

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    puntaje = models.IntegerField()

    def __str__(self):
        return self.texto

