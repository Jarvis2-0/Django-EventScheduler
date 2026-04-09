#pyright: basic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Event
from .forms import EventForm, CustomUserCreationForm


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


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'events/profile.html', {'form': form})



@login_required
def event_list(request):
    events = Event.objects.filter(user= request.user).order_by('date', 'time')
    return render(request, 'events/event_list.html', {'events': events})

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
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event-list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})