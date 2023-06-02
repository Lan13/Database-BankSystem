from django.db import models


# Create your models here.
class BankBranch(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.name}"
