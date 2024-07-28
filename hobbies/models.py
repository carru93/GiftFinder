from django.db import models

from users.models import User


class Hobby(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class UserHobbies(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hobbies = models.ManyToManyField(Hobby)

    def __str__(self):
        return str(self.user)
