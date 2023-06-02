from django.urls import path, include
from . import views

app_name = 'bills'

urlpatterns = [
    path('bills/<int:account_id>/', views.bills, name='bills'),
    path('create/<int:account_id>/', views.create_bill, name='create_bill'),
]
