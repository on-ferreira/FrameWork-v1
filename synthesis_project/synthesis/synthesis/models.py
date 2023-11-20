from django.db import models
from sympy import true

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    poco = models.CharField(max_length=255)
    um = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ProjectData(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    data = models.CharField(max_length=4095)
    timestamp = models.FloatField()


    def __str__(self):
        return f"ProjectData {self.id} - Project {self.project.id} - Timestamp: {self.timestamp}"