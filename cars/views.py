from django.shortcuts import render


def index(request):
    return render(request, "cars/index.html")

def cars(request):
    return render(request, "cars/cars.html")

def contacts(request):
    return render(request, "cars/contacts.html")

def catalog(request):
    return render(request, "cars/catalog.html")