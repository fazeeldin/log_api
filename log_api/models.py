from django.db import models

# Create your models here.
class Logger(models.Model):
    info = models.CharField(max_length=200, default="")
    date = models.DateTimeField()
    date_range = models.CharField(max_length=40, default="")
    
    def __str__(self):
        return self.info