from django.db import models
from branch.models import BankBranch


# Create your models here.
class BranchDepartments(models.Model):
    objects = models.Manager()
    branch = models.ForeignKey(BankBranch, on_delete=models.CASCADE, related_name='BranchDepartments')
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.branch.name}-{self.name}"
