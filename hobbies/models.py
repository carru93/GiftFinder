from django.db import models


class Hobby(models.Model):
    """
    Model representing a hobby.
    Attributes:
        name (CharField): The name of the hobby.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Hobbies"

    def __str__(self):
        return str(self.name)
