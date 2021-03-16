# Create your models here.
from django.db import models

class Predictions(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    fare = models.IntegerField(default=0)
    family_cnt = models.IntegerField()
    Embarked = models.CharField(max_length = 30,default="")
    prediction = models.CharField(max_length =30,default="")
    predicted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name