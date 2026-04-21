#pyright: basic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from .models import Event, Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .forms import EventForm, CustomUserCreationForm, CustomPasswordChangeForm
from django.utils import timezone
from datetime import datetime

# Create your views here.

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   #user login after registration
            messages.success(request, f'Welcome {user.username}! You are Registered & Login Successfully.')

            return redirect('event-list')
        else: 
            form = CustomUserCreationForm()
            return render(request, 'events/register.html', {'form':form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register.html', {'form':form})


@staff_member_required
def admin_dashboard(request):
    users = User.objects.prefetch_related('event_set', 'profile').annotate(
        total_events=Count('event'),
        sent_reminders=Count('event', filter=Q(event__reminder_status='sent')),
        failed_reminders=Count('event', filter=Q(event__reminder_status='failed')),
        pending_reminders=Count('event', filter=Q(event__reminder_status='pending')),
    )
    return render(request, 'events/admin_dashboard.html', {'users': users})




@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # Update email and reminder toggle
            email = request.POST.get('email')
            reminder_enabled = request.POST.get('email_reminder_enabled') == 'on'
            if email:
                request.user.email = email
                request.user.save()
            profile.email_reminder_enabled = reminder_enabled
            profile.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        elif 'change_password' in request.POST:
            # Change password
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # keep logged in
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'events/profile.html', {
        'user': request.user,
        'profile': profile,
        'password_form': form
    })


@login_required
def event_list(request):
    now = timezone.now()
    events = Event.objects.filter(user=request.user)
    upcoming_events = []
    for event in events:
        event_dt = timezone.make_aware(event.start_datetime)
        if event_dt >= now:
            upcoming_events.append(event)
    upcoming_events.sort(key=lambda e: e.start_datetime)
    return render(request, 'events/event_list.html', {'events': upcoming_events})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event-detail', pk=event.pk)
    else:
        form = EventForm(user=request.user)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('event-detail', pk=event.pk)
    else:
        form = EventForm(instance=event, user=request.user)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Update Event'})


@login_required
def event_history(request):
    # Past events: date < today OR (date == today and time < now)
    now = timezone.now()
    events = Event.objects.filter(user=request.user)
    past_events = []
    for event in events:
        event_dt = timezone.make_aware(event.start_datetime)
        if event_dt < now:
            past_events.append(event)
    return render(request, 'events/history.html', {'events': past_events})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})