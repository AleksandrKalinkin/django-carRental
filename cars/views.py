from django.shortcuts import render
from cars.models import Cars, CarsCategory


def index(request):
    context = {
        "title": "CarRentRzn - Аренда автомобилей в Рязани"
    }
    return render(request, "cars/index.html", context)

def cars(request):
    context = {
        "title": "CarRentRzn - Каталог автомобилей",
        "cars": Cars.objects.all(),
        "categories": CarsCategory.objects.all(),
    }
    return render(request, "cars/cars.html", context)

def contacts(request):
    context = {
        "title": "CarRentRzn - Контакты"
    }
    return render(request, "cars/contacts.html", context)

def catalog(request):
    context = {
        "title": "CarRentRzn - Каталог"
    }
    return render(request, "cars/catalog.html", context)