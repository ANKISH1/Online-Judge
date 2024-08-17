from django.db import models

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=50)
    statement = models.CharField(max_length=4000)

    def __str__(self):
        return self.name
