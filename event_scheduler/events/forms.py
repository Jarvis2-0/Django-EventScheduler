#pyright: basic
from django import forms
from .models import Event
from django.utils import timezone

class   EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'time', 'description']
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

        # If updating, exclude the current event from conflict check
        instance = getattr(self, 'instance', None)
        conflict_qs = Event.objects.filter(user=user, date=date, time=time)
        if instance and instance.pk:
            conflict_qs = conflict_qs.exclude(pk=instance.pk)

        if conflict_qs.exists():
            raise forms.ValidationError("You already have an event on this date and time. No scheduling conflicts allowed.")

        return cleaned_data


