import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from .models import Pages

def annotatedView(request, identificador):
    if request.user.is_authenticated():
        respuesta = "<p id='user'>Logged in as " + str(request.user.username) + ". <a href='/logout'>Logout</a></p><br>"
    else:
        respuesta = "<p id='user'>Not logged in. <a href='/login'>Login</a></p><br>"
    try:
        pag = Pages.objects.get(id=identificador)
        respuesta += pag.page
    except Pages.DoesNotExist:
        respuesta += "Pagina no existente"
    respuesta += "<h3>Si quieres puedes cambiar el contenido</h3>"
    respuesta += "<form action='/pagina/" + str(pag.id) + "'method='post'>"
    respuesta += "Nuevo contenido:<input type='text' name='content' value=''>"
    respuesta += "<input type='submit' value='Change'></form>"
    template = get_template("index.html")
    argumentos = Context({'contenido': respuesta})
    return HttpResponse(template.render(argumentos))

@csrf_exempt
def mostrar (request, identificador):
    if request.user.is_authenticated():
        respuesta = "Logged in as " + str(request.user.username) + ". <a href='/logout'>Logout</a><br>"
    else:
        respuesta = "Not logged in. <a href='/login'>Login</a><br>"
    try:
        pag = Pages.objects.get(id=identificador)
        if request.method == "GET":
            respuesta += "<h2>Pagina:</h2> " + pag.page
            if request.user.is_authenticated():
                respuesta += "<h3>Si quieres puedes cambiar el contenido</h3>"
                respuesta += "<form action='/pagina/" + str(pag.id) + "'method='post'>"
                respuesta += "Nuevo contenido:<input type='text' name='content' value=''>"
                respuesta += "<input type='submit' value='Change'></form>"
        elif request.method == "POST":
            if request.user.is_authenticated():
                content = request.POST.get('content')
                pag.page = content
                pag.save()
            respuesta += "Tus cambios han sido guardados con exito"
        else:
            respuesta += "Metodo no valido"
        respuesta += '<br><a href="/">Home</a>'
    except Pages.DoesNotExist:
        respuesta = "Pagina no existente"
    return HttpResponse (respuesta)

def listar ():
    lista_paginas = Pages.objects.all()
    respuesta =" Las paginas son: </br>"
    for paginas in lista_paginas:
        respuesta +=  "Nombre de la pagina: "  + str(paginas.name) + "-><a href='pagina/"+str(paginas.id)+"'>Normal</a>"
        respuesta += "<span>;      </span><a href='annotated/"+str(paginas.id)+"'>Template</a><br>"
    return str(respuesta)

def inicio(request):
    value = ""
    if request.user.is_authenticated():
        value += "Logged in as " + str(request.user.username) + ". <a href='/logout'>Logout</a>"
    else:
        value += "Not logged in. <a href='/login'>Login</a>"
    value += "<br>" + listar()
    return HttpResponse(value)

def user_login(request):
    value = "Welcome " + request.user.username
    value += '<br><a href="/">Home</a>'
    return HttpResponse(value)

def user_logout(request):
    if request.user.is_authenticated():
        value = "Logout " + str(request.user.username)
        logout(request)
        value += '<br><a href="/">Home</a>'
    else:
        value = '<a href="/">Home</a>'
    return HttpResponse(value)

def notFound(request):
    value = "Recurso no disponible"
    value += '<br><a href="/">Home</a>'
    return HttpResponse(value)
