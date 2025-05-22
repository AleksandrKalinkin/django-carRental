from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars.views import index, contacts, catalog, reviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('cars/', include("cars.urls", namespace="cars")),
    path('users/', include("users.urls", namespace="users")),
    path('contacts/', contacts, name="contacts"),
    path('reviews/', reviews, name='reviews'),

    # Аутентификация
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Сброс пароля (ваши существующие настройки)
    path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name='users/password_reset_form.html',
         email_template_name='users/password_reset_email.html',
         subject_template_name='users/password_reset_subject.txt',
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='users/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='users/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='users/password_reset_complete.html',
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)