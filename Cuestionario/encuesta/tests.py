from django.test import TestCase
from django.urls import reverse
from .form import UserInfoForm
from .models import Seccion, Pregunta, Respuesta



#Vista: principal()
class PrincipalViewTests(TestCase):
    
    # Prueba que la vista se renderiza correctamente con una solicitud GET
    def test_principal_view_get(self):
        response = self.client.get(reverse('principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'principal.html')
        self.assertIsInstance(response.context['form'], UserInfoForm)
        


    # Prueba que la vista redirige correctamente con una solicitud POST valida
    def test_principal_view_post_valid(self):
        data = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'dni': 12345678
        }
        response = self.client.post(reverse('principal'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['nombre'], 'Juan')
        self.assertEqual(self.client.session['apellido'], 'Perez')
        self.assertEqual(self.client.session['dni'], 12345678)

    
    
    # Prueba que la vista maneja correctamente una solicitud POST invalida
    def test_principal_view_post_invalid(self):
        data = {
            'nombre': '', # Campo vacio para forzar el error
            'apellido': 'Perez',
            'dni': '12345678'
        }
        response = self.client.post(reverse('principal'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'principal.html')
        self.assertFalse(response.context['form'].is_valid())







# Vista: renderizar_pregunta()
class RenderizarPreguntaViewTests(TestCase):

    # Crear objetos de prueba en una base de datos temporal
    def setUp(self):
        self.seccion = Seccion.objects.create(nombre='Sección 1')
        self.pregunta = Pregunta.objects.create(seccion=self.seccion, texto='¿Pregunta 1?')
        self.respuesta1 = Respuesta.objects.create(pregunta=self.pregunta, texto='Respuesta 1', puntaje=1)
        self.respuesta2 = Respuesta.objects.create(pregunta=self.pregunta, texto='Respuesta 2', puntaje=2)
        self.respuesta3 = Respuesta.objects.create(pregunta=self.pregunta, texto='Respuesta 3', puntaje=3)
    

    
    # Prueba que la vista se renderiza correctamente con una solicitud GET
    def test_renderizar_pregunta_view_get(self):
        url = reverse('renderizar_pregunta', args=[self.seccion.id, self.pregunta.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'seccion1.html')
        self.assertEqual(response.context['seccion'], self.seccion)
        self.assertEqual(response.context['pregunta_actual'], self.pregunta)

        respuestas_en_template = list(response.context['respuestas'].order_by('id'))
        respuestas_en_prueba = list(self.pregunta.respuesta_set.all().order_by('id'))
        self.assertQuerysetEqual(respuestas_en_template, respuestas_en_prueba, transform=lambda x: x)

        self.assertEqual(response.context['puntaje_total'], 0)

    
    
    # Prueba que la vista usa correctamente los datos de la sesion
    def test_renderizar_pregunta_view_get_with_session_data(self):
        session = self.client.session
        session['puntaje_total'] = 10
        session.save()

        url = reverse('renderizar_pregunta', args=[self.seccion.id, self.pregunta.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['puntaje_total'], 10)

