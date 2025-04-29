from django.contrib.auth.forms import AuthenticationForm
from users.models import User

class UserLoginForm(AuthenticationForm): #создаем дочерний класс
    class Meta: #Дочерний класс Meta- в качестве базовой модели будет использоваться user из user/models
        model = User
        fields = ('username', 'password') #нам нужны только эти поля при авторизации, а год рождения и тд - не нужно
