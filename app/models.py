from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class QatagonlarClassModel(models.Model):
    full_name = models.CharField(max_length=200)
    bio = models.TextField()
    birth_year = models.DateField()
    died_year = models.DateField()
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
