from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/<int:user_id>/', views.create_account, name='create_account'),
    path('accounts/<int:user_id>/', views.accounts, name='accounts'),
    path('delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('transfer/<int:account_id>/', views.transfer, name='transfer'),
]
