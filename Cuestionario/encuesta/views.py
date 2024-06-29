from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Seccion, Pregunta, Respuesta
from .form import UserInfoForm


def principal(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            # Guardar los datos en la sesión
            request.session['nombre'] = form.cleaned_data['nombre']
            request.session['apellido'] = form.cleaned_data['apellido']
            request.session['dni'] = form.cleaned_data['dni']
            return redirect('home')  # Redirigir a la vista principal del cuestionario
    else:
        form = UserInfoForm()
    return render(request, 'principal.html', {'form': form})



def home(request):
    return render(request, 'home.html')



def final_cuestionario(request):
    return render(request, 'final_cuestionario.html', {})



def renderizar_pregunta(request, seccion_id, pregunta_id):
    seccion = get_object_or_404(Seccion, pk=seccion_id)
    pregunta_actual = get_object_or_404(Pregunta, pk=pregunta_id)
    respuestas = pregunta_actual.respuesta_set.all()
    
    context = {
        'seccion': seccion,
        'pregunta_actual': pregunta_actual,
        'respuestas': respuestas,
        'puntaje_total': request.session.get('puntaje_total', 0),
    }
    return render(request, 'seccion1.html', context)



def enviar_resultados_por_correo(puntajes_secciones, puntaje_total, destinatario,nombre,apellido,dni):
    subject = 'Resultados del Cuestionario'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [destinatario]
    context = {
        'puntajes_secciones': puntajes_secciones,
        'puntaje_total': puntaje_total,
        'nombre':nombre,
        'apellido':apellido,
        'dni':dni,
    }
    
    # Renderizar el contenido del correo electrónico usando un template
    message = render_to_string('resultados.html', context)
    
    # Enviar el correo electrónico
    send_mail(subject, '', from_email, recipient_list, html_message=message)




def enviar_email(request):
    if request.method == 'POST':
        # Obtener los puntajes de las secciones y el puntaje total desde la sesión
        puntajes_secciones = request.session.get('puntajes_secciones', {
            'seccion1': 0,
            'seccion2': 0,
            'seccion3': 0,
            'seccion4': 0,
            'seccion5': 0,
            'seccion6': 0,
        })
        puntaje_total = request.session.get('puntaje_total', 0)

        nombre = request.session.get('nombre', 'N/A')
        apellido = request.session.get('apellido', 'N/A')
        dni = request.session.get('dni', 'N/A')
        
        # Dirección de correo electrónico del destinatario
        destinatario = 'mlaclau@santabarbarasa.com.ar'
        
        # Enviar los resultados por correo electrónico
        enviar_resultados_por_correo(puntajes_secciones, puntaje_total, destinatario,nombre,apellido,dni)
        
        # Resetear los valores en la sesión
        request.session['puntajes_secciones'] = {
            'seccion1': 0,
            'seccion2': 0,
            'seccion3': 0,
            'seccion4': 0,
            'seccion5': 0,
            'seccion6': 0,
        }
        request.session['puntaje_total'] = 0
        request.session['nombre'] = ''
        request.session['apellido'] = ''
        request.session['dni'] = ''
        request.session.modified = True
        
        # Redirigir a la página de inicio o una página de confirmación
        return redirect('principal')  



def procesar_respuesta(request, seccion_id):
    try:
        if request.method == 'POST':
            pregunta_id = request.POST.get('pregunta_id')
            respuesta_id = request.POST.get('respuesta')

            pregunta_actual = get_object_or_404(Pregunta, pk=pregunta_id)
            respuesta = get_object_or_404(Respuesta, pk=respuesta_id)

            # Inicializar el diccionario de respuestas en la sesión si no existe
            if 'respuestas' not in request.session:
                request.session['respuestas'] = {}

            # Guardar la puntuación de la respuesta actual
            request.session['respuestas'][pregunta_id] = respuesta.puntaje

            # Inicializar los acumuladores de puntajes por sección si no existen
            if 'puntajes_secciones' not in request.session:
                request.session['puntajes_secciones'] = {}

            puntajes_secciones = request.session['puntajes_secciones']

            # Asegurarse de que cada clave de sección está inicializada
            if 'seccion1' not in puntajes_secciones:
                puntajes_secciones['seccion1'] = 0
            if 'seccion2' not in puntajes_secciones:
                puntajes_secciones['seccion2'] = 0
            if 'seccion3' not in puntajes_secciones:
                puntajes_secciones['seccion3'] = 0
            if 'seccion4' not in puntajes_secciones:
                puntajes_secciones['seccion4'] = 0
            if 'seccion5' not in puntajes_secciones:
                puntajes_secciones['seccion5'] = 0
            if 'seccion6' not in puntajes_secciones:
                puntajes_secciones['seccion6'] = 0
            if 'puntaje_total' not in puntajes_secciones:
                puntajes_secciones['puntaje_total'] = 0

            # Acumular el puntaje en la sección correspondiente
            if seccion_id == 1:
                puntajes_secciones['seccion1'] += respuesta.puntaje
            elif seccion_id == 2:
                puntajes_secciones['seccion2'] += respuesta.puntaje
            elif seccion_id == 3:
                puntajes_secciones['seccion3'] += respuesta.puntaje
            elif seccion_id == 4:
                puntajes_secciones['seccion4'] += respuesta.puntaje
            elif seccion_id == 5:
                puntajes_secciones['seccion5'] += respuesta.puntaje
            elif seccion_id == 6:
                puntajes_secciones['seccion6'] += respuesta.puntaje

            puntajes_secciones['puntaje_total'] = puntajes_secciones['seccion1'] + puntajes_secciones['seccion2'] + puntajes_secciones['seccion3'] + puntajes_secciones['seccion4'] + puntajes_secciones['seccion5'] + puntajes_secciones['seccion6']              

            # Guardar el diccionario actualizado en la sesión
            request.session['puntajes_secciones'] = puntajes_secciones
            request.session.modified = True

            # Verificar el estado de la sesión
            print(f'Sesión actualizada: {request.session["puntajes_secciones"]}')

            seccion = get_object_or_404(Seccion, pk=seccion_id)
            siguiente_pregunta = Pregunta.objects.filter(seccion=seccion, id__gt=pregunta_actual.id).order_by('id').first()

            if siguiente_pregunta:
                return redirect('renderizar_pregunta', seccion_id=seccion_id, pregunta_id=siguiente_pregunta.id)
            else:
                siguiente_seccion = Seccion.objects.filter(id__gt=seccion_id).order_by('id').first()
                if siguiente_seccion:
                    return redirect('renderizar_pregunta', seccion_id=siguiente_seccion.id, pregunta_id=siguiente_seccion.pregunta_set.first().id)
                else:
                    return redirect('final_cuestionario')
    except Exception as e:
        print(f'Error: {e}')
        messages.error(request, "Debe seleccionar una respuesta para poder avanzar.")
    
    return redirect('renderizar_pregunta', seccion_id=seccion_id, pregunta_id=pregunta_id)










