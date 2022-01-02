from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class Collection:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

collections = [
    Collection('Original Adidas Logo', 'The very first Adidas logo', 150000),
    Collection('UFC Poster', 'Poster for the very first UFC event', 1000000),
    Collection('Jimi Hendrix Guitar', "Jimi Hendrix's Guitar from Woodstock", 950)
]

def collections_index(request):
    return render(request, 'collections/index.html', { 'collections': collections })