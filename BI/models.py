from django.db import models


class Request(models.Model):
    datetime = models.DateTimeField()
    rmse = models.FloatField()
    mae = models.FloatField()
    mape = models.FloatField()


class CSVFile(models.Model):
    namefile = models.TextField()
    filecontent = models.TextField()
    countrows = models.IntegerField()
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)


class Monitoring(models.Model):
    memory = models.FloatField()
    cpu = models.FloatField()
    time = models.FloatField()
    request = models.OneToOneField(Request, on_delete=models.CASCADE, primary_key=True)
