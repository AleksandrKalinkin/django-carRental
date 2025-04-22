from django.urls import path
from cars.views import cars

app_name = "cars" #название файла


urlpatterns = [
    path('', cars, name = "index"),

]
