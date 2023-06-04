from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ConstructItem(models.Model):
    construct_number = models.CharField(max_length=50)
    receptor = models.CharField(max_length=100)
    DNA_sequence = models.TextField()
    description = models.TextField()
    comment = models.TextField()
    user = models.TextField()
    application_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.construct_number

class ApplicationItem(models.Model):
    construct_number = models.CharField(max_length=50)
    P = models.IntegerField()
    biomass = models.IntegerField()
    expression_system = models.CharField(max_length=100)
    #construct_item = models.ForeignKey(ConstructItem, on_delete=models.CASCADE)
    application_user = models.CharField(max_length=100)
    comment = models.TextField()
    application_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.construct_number} - {self.application_time}"
