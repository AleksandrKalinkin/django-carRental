from django.db import models

# Create your models here.

# модель = таблица

class CarsCategory(models.Model):
    name = models.CharField(max_length = 64, unique=True) #название категории уникально - поэтому True
    description = models.TextField(blank=True)# Здесь blank=True,это значит, что поле description м.б и не заполненым

    def __str__(self):
        return self.name

class Cars(models.Model):
    name = models.CharField(max_length = 256)
    image = models.ImageField(upload_to="cars_media") #из папки cars_media будут грузиться фотки
    description = models.TextField(blank=True)  # Здесь blank=True,это значит, что поле description м.б и не заполненым
    short_description = models.TextField(max_length=64, blank=True)  # Здесь blank=True,это значит, что поле description м.б и не заполненым
    price = models.DecimalField(max_digits=7, decimal_places=2) #5- так как у меня цена тачки за сутки максимум 30000.00 будет, 2 - так как.00
    category = models.ForeignKey(CarsCategory, on_delete= models.PROTECT)#внешний ключ из таблицы

    def __str__(self):
        return f"{self.name} | {self.category.name}"
