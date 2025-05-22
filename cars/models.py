from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# модель = таблица

class CarsCategory(models.Model):
    name = models.CharField(max_length = 64, unique=True) #название категории уникально - поэтому True
    description = models.TextField(blank=True)# Здесь blank=True,это значит, что поле description м.б и не заполненым

    class Meta:
        verbose_name_plural = "Categories" #убираем S в админке на конце

    def __str__(self):
        return self.name

class Cars(models.Model):
    name = models.CharField(max_length = 256)
    image = models.ImageField(upload_to="cars_media") #из папки cars_media будут грузиться фотки
    description = models.TextField(blank=True)  # Здесь blank=True,это значит, что поле description м.б и не заполненым
    short_description = models.TextField(max_length=64, blank=True)  # Здесь blank=True,это значит, что поле description м.б и не заполненым
    price = models.DecimalField(max_digits=7, decimal_places=2) #5- так как у меня цена тачки за сутки максимум 30000.00 будет, 2 - так как.00
    category = models.ForeignKey(CarsCategory, on_delete= models.PROTECT, related_name='cars')#внешний ключ из таблицы

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey('Cars', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    child_seat = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено')
    ])

    def __str__(self):
        return f"{self.name} | {self.category.name}"

    class Meta:
        verbose_name_plural = "Cars" #убираем S в админке на конце
