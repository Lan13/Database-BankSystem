from django.db import models
from users.models import BankUser
from branch.models import BankBranch
from django.core.validators import MinValueValidator


# Create your models here.
class UserAccounts(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(BankUser, on_delete=models.CASCADE, related_name='UserAccounts')
    branch = models.ForeignKey(BankBranch, on_delete=models.CASCADE, related_name='BranchAccounts', null=True)
    account_id = models.AutoField(primary_key=True)
    money = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"账户号{self.account_id}-{self.user.name}"