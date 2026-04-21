from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_event_reminder(self, event_id):
    try:
        event = Event.objects.select_related('user', 'user__profile').get(pk=event_id)
        if event.reminder_status != 'pending':
            return f"Reminder already {event.reminder_status} for event {event_id}"
        
        # Check if user wants reminders
        if not event.user.profile.email_reminder_enabled:
            event.reminder_status = 'failed'
            event.save(update_fields=['reminder_status'])
            return f"User {event.user.username} disabled reminders"
        
        if not event.user.email:
            event.reminder_status = 'failed'
            event.save(update_fields=['reminder_status'])
            return f"User {event.user.username} has no email"
        
        send_mail(
            subject=f'Reminder: {event.name} is soon!',
            message=f'Your event "{event.name}" is scheduled at {event.time} on {event.date}.\n\nDescription: {event.description}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[event.user.email],
            fail_silently=False,
        )
        event.reminder_status = 'sent'
        event.reminder_sent_at = timezone.now()
        event.save(update_fields=['reminder_status', 'reminder_sent_at'])
        return f"Reminder sent for {event.name} to {event.user.email}"
    
    except Exception as e:
        # Update status to failed
        Event.objects.filter(pk=event_id).update(reminder_status='failed')
        # Retry after 5 minutes, up to 3 times
        raise self.retry(exc=e, countdown=300)

@shared_task
def check_upcoming_events():
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)
    events = Event.objects.filter(reminder_status='pending')
    for event in events:
        event_datetime = timezone.make_aware(event.start_datetime)
        if now <= event_datetime <= one_hour_later:
            send_event_reminder.delay(event.pk)
    return "Queued reminders"