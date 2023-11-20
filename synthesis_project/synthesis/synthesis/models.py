from django.db import models
from sympy import true

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    poco = models.CharField(max_length=255)
    um = models.CharField(max_length=255)
    link_dados_rto = models.CharField(max_length=255)

    def __str__(self):
        return self.name