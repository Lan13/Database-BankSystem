from django.db import models
from accounts.models import UserAccounts


# Create your models here.
class AccountBills(models.Model):
    bill_type = [
        ('收入', '收入'),
        ('支出', '支出'),
    ]
    objects = models.Manager()
    account = models.ForeignKey(UserAccounts, on_delete=models.CASCADE, related_name='AccountBills')
    bill_id = models.AutoField(primary_key=True)
    changes = models.FloatField()
    type = models.CharField(max_length=100, choices=bill_type, default='收入')
    remark = models.CharField(max_length=1000, default='', blank=True)
    money = models.FloatField(default=0)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"账单号{self.bill_id}-账户号{self.account.account_id}-{self.account.user.name}"
