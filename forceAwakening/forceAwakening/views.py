from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>Who are you?</h1>\n<br><a href='/recruit/'>Im a recruit</a><br>\n<a href='/recruit/sith/'>Im a sith</a>")