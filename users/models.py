from django.db import models
from django.contrib.auth.models import AbstractUser # унаследуем users из админки, так как там он уже есть

#Дочерний класс от AbstractUser (от Django - auth.models)
class User(AbstractUser):
    #Добавляем новое поле - фото (они будут храниться в media/users_images)
    image = models.ImageField(upload_to="users_images", blank=True)




