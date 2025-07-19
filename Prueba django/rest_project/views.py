from django import HttpResponse
from django.shortcuts import render

def funcion_respuesta_a_solicitud2(request):
    return HttpResponse("esta es la respuesta a la <b>solicitud2</b> desde una función en views.py")

def funcion_respuesta_a_solicitud3(request):
    return render(request, 'respuesta_solicitud3.html')
