from django import forms
from django.utils import timezone

from .models import Project, Client


class EntryForm(forms.Form):
    start = forms.DateTimeField(label="Start Time", help_text="Format: 2006-10-25 14:30")
    end = forms.DateTimeField(label="End Time", help_text="Format: 2006-10-25 14:30")
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    description = forms.CharField()

    def clean_start(self):
        now = timezone.now()
        start = self.cleaned_data['start']
        if start > now:
            raise forms.ValidationError("Start time for this entry must be in the past")
        return start

    def clean_end(self):
        now = timezone.now()
        end = self.cleaned_data['end']
        if end > now:
            raise forms.ValidationError("End time for this entry must be in the past")
        return end

    def clean(self):
        start = self.data['start']
        end = self.data['end']
        if start > end:
            raise forms.ValidationError("The end time for this entry must be after the start time")
        return data

# We so need to use a ModelForm here...
class ProjectForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    name = forms.CharField()

# and here...
class ClientForm(forms.Form):
    name = forms.CharField()
