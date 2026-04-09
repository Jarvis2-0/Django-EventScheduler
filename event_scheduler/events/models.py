#pyright: basic
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    date= models.DateField()
    time= models.TimeField()
    description= models.TextField(blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"
    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.pk)])

