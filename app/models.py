from django.db import models

class AppModel(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=50)
    # param = models.CharField(max_length=250)
    #values = models.CharField(max_length=250)


