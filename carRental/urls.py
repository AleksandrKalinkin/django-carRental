"""
URL configuration for carRental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from cars.views import index
from cars.views import contacts
from cars.views import catalog
from django.urls import path
from cars import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"), #добавили индекс
    path('cars/', include("cars.urls", namespace="cars")), #добавили cars
    path('users/', include("users.urls", namespace="users")), #добавили users
    path('contacts/', contacts, name="contacts"),
    path('catalog/', catalog, name="catalog"),
    path('reviews/', views.reviews, name='reviews'),
    path('users/', views.reviews, name='users.urls'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)