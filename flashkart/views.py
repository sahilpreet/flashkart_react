from django.http import HttpResponse
from django.shortcuts import render

def index(response):
    return HttpResponse("<h1>hello world, Index page of flashkat in django-admin not in app</h1>")