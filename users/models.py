from django.db import models
from django.contrib.auth.models import AbstractUser # унаследуем users из админки, так как там он уже есть

#Дочерний класс от AbstractUser (от Django - auth.models)
class User(AbstractUser):
    #Добавляем новое поле - фото (они будут храниться в media/users_images)
    image = models.ImageField(upload_to="users_images", blank=True)
    email = models.EmailField(
        unique=True,  # Уникальность на уровне БД
        error_messages={
            'unique': "Пользователь с таким email уже существует"
        }
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True,
                                    error_messages={
                                                    'unique': "Этот номер телефона уже зарегистрирован"
                                                    })  # Добавляем телефон
    birth_day = models.DateField(blank=True, null=True)  # Добавляем дату рождения




