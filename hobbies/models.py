from django.db import models


class Hobby(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Hobbies"

    def __str__(self):
        return str(self.name)
