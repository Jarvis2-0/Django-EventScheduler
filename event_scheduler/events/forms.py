from django import forms
from .models import Event
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        user = self.user
        instance = getattr(self, 'instance', None)
        conflict_qs = Event.objects.filter(user=user, date=date, time=time)
        if instance and instance.pk:
            conflict_qs = conflict_qs.exclude(pk=instance.pk)
        if conflict_qs.exists():
            raise forms.ValidationError("You already have an event on this date and time.")
        return cleaned_data
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. We will send reminders to this email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
