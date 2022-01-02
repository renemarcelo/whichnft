from django.shortcuts import render
from .models import Collection
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def collections_index(request):
    collections = Collection.objects.all()
    return render(request, 'collections/index.html', { 'collections': collections })

def collections_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    return render(request, 'collections/detail.html', { 'collection': collection })
