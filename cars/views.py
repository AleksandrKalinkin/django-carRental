from django.shortcuts import render, get_object_or_404
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

def reviews(request):
    return render(request, 'cars/reviews.html')

def car_card(request, car_id):
    car = get_object_or_404(Cars, pk=car_id)
    context = {
        'car': car,
        'title': f"{car.name} {car.category}"
    }
    return render(request, 'cars/car_card.html', context)