from django.shortcuts import render
from django.http import JsonResponse

def api_data_view(request):
    data = {
        'message': '¡Dato enviado desde  el backend!',
    }
    return JsonResponse(data)
