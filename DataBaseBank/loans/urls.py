from django.urls import path, include
from . import views

app_name = 'loans'

urlpatterns = [
    path('apply_loan/<int:user_id>/', views.apply_loan, name="apply_loan"),
    path('loans/<int:user_id>/', views.loans, name="loans"),
    path('delete_loan/<int:loan_id>/', views.delete_loan, name="delete_loan"),
    path('pay_loan/<int:loan_id>/', views.pay_loan, name="pay_loan"),
]
