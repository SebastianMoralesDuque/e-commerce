from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import os


from django.core.files.storage import default_storage
from django.http import JsonResponse

from django.core.files.storage import default_storage

def guardar_imagen(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']
        nombre_imagen = imagen.name  # Obtener el nombre de la imagen original
        ruta_guardado = 'productos/' + nombre_imagen  # Ruta personalizada donde se guardará la imagen

        # Guardar la imagen en la ubicación personalizada
        default_storage.save(ruta_guardado, imagen)

        # Devolver una respuesta adecuada al cliente (por ejemplo, un JSON con la ruta de la imagen guardada)
        return JsonResponse({'ruta': ruta_guardado})
    else:
        # Devolver una respuesta de error si no se proporcionó una imagen
        return JsonResponse({'error': 'No se proporcionó una imagen'}, status=400)


def productos_fotos_view(request, path):
    # Obtener la ruta absoluta al archivo de imagen
    absolute_path = os.path.join(settings.MEDIA_ROOT, 'productos', path)

    try:
        with open(absolute_path, 'rb') as file:
            # Leer el contenido del archivo
            file_content = file.read()

        # Crear una respuesta HTTP con el contenido del archivo
        return HttpResponse(file_content, content_type='image/jpeg')
    except IOError:
        # Si el archivo no existe, devolver una respuesta 404
        return HttpResponse(status=404)
