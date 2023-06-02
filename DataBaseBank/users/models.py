from django.db import models
from django.contrib.auth.models import User
from branch.models import BankBranch


# Create Bank User Information
class BankUser(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='BankUser', null=True)
    branch = models.ForeignKey(BankBranch, on_delete=models.CASCADE, related_name='BranchUser', null=True)
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    counts = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}-{self.name}"
