from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.bank_user_register, name='register'),
    path('change_pwd/<int:user_id>/', views.change_pwd, name='change_pwd'),
    path('edit/<int:user_id>/', views.bank_user_edit, name="edit"),
    path('get_users/', views.get_users, name='get_users'),
]
