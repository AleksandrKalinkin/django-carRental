from django.contrib import admin

# Register your models here.


from cars.models import Cars, CarsCategory

admin.site.register(Cars)
admin.site.register(CarsCategory)