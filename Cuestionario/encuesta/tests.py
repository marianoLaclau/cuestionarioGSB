# tests.py
from django.test import TestCase
from django.urls import reverse
from .form import UserInfoForm


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
            'dni': '12345678'
        }
        response = self.client.post(reverse('principal'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['nombre'], 'Juan')
        self.assertEqual(self.client.session['apellido'], 'Perez')
        self.assertEqual(self.client.session['dni'], '12345678')

    
    
    # Prueba que la vista maneja correctamente una solicitud POST invalida
    def test_principal_view_post_invalid(self):
        data = {
            'nombre': '',
            'apellido': 'Perez',
            'dni': '12345678'
        }
        response = self.client.post(reverse('principal'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'principal.html')
        self.assertFalse(response.context['form'].is_valid())



