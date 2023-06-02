from django.urls import path, include
from . import views

app_name = 'departments'

urlpatterns = [
    path('departments/', views.departments, name='departments'),
    path('staffs/<int:department_id>/', views.department_staffs, name='department_staffs'),
]
