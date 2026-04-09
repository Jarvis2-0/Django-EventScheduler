from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Event

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Event

@shared_task
def send_event_reminder(event_id):
    """Send a reminder email for a specific event (only if user has an email)"""
    try:
        event = Event.objects.get(id=event_id)
        if not event.reminder_sent:
            # ✅ Check if the user has an email address
            if event.user.email:
                send_mail(
                    subject=f'Reminder: {event.name} is today!',
                    message=f'Your event "{event.name}" is scheduled at {event.time} on {event.date}.\n\nDescription: {event.description}',
                    from_email='noreply@eventscheduler.com',
                    recipient_list=[event.user.email],
                    fail_silently=False,
                )
                event.reminder_sent = True
                event.save()
                return f"Reminder sent for event {event.pk} to {event.user.email}"
            else:
                return f"User {event.user.username} has no email – reminder not sent for event {event.pk}"
    except Event.DoesNotExist:
        return f"Event {event_id} not found"
    return "Reminder already sent or error"

@shared_task
def check_upcoming_events():
    """Run periodically to find events starting in next 1 hour and queue reminders"""
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)
    # Find events whose start_datetime is between now and one_hour_later
    # Since we have separate date+time, we combine in Python; for performance, add a start_datetime field to model.
    events = Event.objects.filter(reminder_sent=False)
    for event in events:
        event_datetime = timezone.make_aware(event.start_datetime)  # if naive
        if now <= event_datetime <= one_hour_later:
            send_event_reminder.delay(event.pk)
    return f"Queued reminders for upcoming events"