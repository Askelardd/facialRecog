from django.db import models

class Pessoa(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='fotos/')
