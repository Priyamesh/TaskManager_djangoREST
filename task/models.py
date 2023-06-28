from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField()
    status = models.CharField(choices=(('completed','COMPLETED'),('pending','PENDING')),max_length=20)

    def __str__(self):
        return self.name
