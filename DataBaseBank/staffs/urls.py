from django.urls import path, include
from . import views

app_name = 'staffs'

urlpatterns = [
    # path('staffs/', views.staffs, name='staffs'),
    path('edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('create/<int:department_id>/', views.create_staff, name='create_staff'),
    path('delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('set_manager/<int:staff_id>/<int:department_id>/', views.set_manager, name='set_manager'),
    path('delete_manager/<int:department_id>/', views.delete_manager, name='delete_manager'),
]
