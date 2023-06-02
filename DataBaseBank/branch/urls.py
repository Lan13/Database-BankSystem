from django.urls import path, include
from . import views

app_name = 'branches'

urlpatterns = [
    path('branches/', views.branches, name='branches'),
]
