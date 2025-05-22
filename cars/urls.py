from django.urls import path
from django.contrib.auth import views as auth_views
from cars.views import (
    index,
    cars,
    car_card,
    catalog,
    contacts,
    reviews,
    booking_history
)

app_name = "cars"


urlpatterns = [
    # Основные URL
    path('', cars, name="index"),
    path('cars/', cars, name="cars"),
    path('catalog/', catalog, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('reviews/', reviews, name='reviews'),

    # URL для работы с автомобилями
    path('car/<int:car_id>/', car_card, name='car_card'),

    # URL для бронирования и истории заказов
    path('booking-history/', booking_history, name='booking_history'),


]