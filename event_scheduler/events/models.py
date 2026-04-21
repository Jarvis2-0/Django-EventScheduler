from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_reminder_enabled = models.BooleanField(default=True)
    # You can add more fields later

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # For existing users without profile, create one
        Profile.objects.get_or_create(user=instance)


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)   # to avoid duplicate reminders
    reminder_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')],
        default='pending'
    )
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    # For accurate reminder calculation, combine date+time into one field (optional but recommended)
    # We'll keep separate fields but combine in a property.

    def __str__(self):
        return f"{self.name} on {self.date} at {self.time}"

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.pk)])

    @property
    def start_datetime(self):
        return datetime.combine(self.date, self.time)