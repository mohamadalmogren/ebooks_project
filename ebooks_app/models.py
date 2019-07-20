from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)

    genders = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = models.CharField(max_length=1, choices=genders)

    def __str__(self):
        return self.user.username

class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    author = models.CharField(max_length=30)
    publish_on = models.DateTimeField(default=timezone.now)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='book_pics')
    about = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])
        