from django.db import models
from branch.models import BankBranch
from users.models import BankUser
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta


# Create your models here.
class Loans(models.Model):
    loan_choices = [
        ('未还清', '未还清'),
        ('已还清', '已还清'),
    ]
    objects = models.Manager()
    loan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BankUser, on_delete=models.CASCADE, related_name='UserLoans')
    branch = models.ForeignKey(BankBranch, on_delete=models.CASCADE, related_name='BranchLoans')
    money = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    remain_money = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=datetime.now() + timedelta(days=365))
    status = models.CharField(max_length=100, choices=loan_choices, default='未还清')

    def __str__(self):
        return f"贷款号{self.loan_id}-{self.user.name}"
