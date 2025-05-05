from django.urls import path
from cars.views import cars, car_card, catalog

app_name = "cars" #название файла


urlpatterns = [
    path('', cars, name = "index"),
    path('catalog/', catalog, name='catalog'),
    path('car/<int:car_id>/', car_card, name='car_card'),

]
