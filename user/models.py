from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=18)
    profile_pic = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.id} - {self.name}'
