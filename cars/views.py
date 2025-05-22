from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Cars, CarsCategory, Booking
from cars.forms import BookingForm


def index(request):
    context = {
        "title": "CarRentRzn - Аренда автомобилей в Рязани"
    }
    return render(request, "cars/index.html", context)


def cars(request):
    category_id = request.GET.get('category')
    cars_list = Cars.objects.all()

    if category_id:
        cars_list = cars_list.filter(category_id=category_id)

    context = {
        "title": "CarRentRzn - Каталог автомобилей",
        "cars": cars_list,
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


@login_required
def car_card(request, car_id):
    car = get_object_or_404(Cars, pk=car_id)


    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # Расчет количества дней и суммы
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                days = (end_date - start_date).days + 1
                total_price = days * car.price

                if form.cleaned_data['child_seat']:
                    total_price += 500 * days

                # Создание бронирования
                Booking.objects.create(
                    user=request.user,
                    car=car,
                    start_date=start_date,
                    end_date=end_date,
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                    child_seat=form.cleaned_data['child_seat'],
                    total_price=total_price,
                    status='pending'
                )

                messages.success(request,
                                 'Бронирование прошло успешно, ожидайте звонка от администратора для подтверждения брони')
                return redirect('cars:booking_history')

            except Exception as e:
                messages.error(request, f'Произошла ошибка: {str(e)}')
    else:
        # Автозаполнение данных пользователя
        initial_data = {
            'first_name': request.user.first_name or '',
            'last_name': request.user.last_name or '',
            'phone': request.user.phone_number or '',
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=1)).date(),
            'start_time': '09:00',
            'end_time': '09:00'
        }
        form = BookingForm(initial=initial_data)

    context = {
        'car': car,
        'form': form,
        'title': f"{car.name} {car.category}",
        'car_price': float(car.price)
    }
    return render(request, 'cars/car_card.html', context)


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'title': 'История бронирований',
        'bookings': bookings
    }
    return render(request, 'cars/booking_history.html', context)