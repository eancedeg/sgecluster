from django.db import models

# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=(
        ('RUNNING', 'running'),
        ('FINISHED', 'finished'),
        ('FAILURE', 'failure')
    ))
    input_file = models.FileField(upload_to='calcs')
    job = models.FileField(upload_to='jobs')
    pid = models.IntegerField()
