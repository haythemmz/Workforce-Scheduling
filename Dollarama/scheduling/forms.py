from django import forms
from django.forms import formset_factory
from .models import Employee,Store,EmployeeAvailability,StoreHours,DAY_CHOICES


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'birthday', 'min_working_hours_weekly', 'max_working_hours_weekly']

class EmployeeAvailabilityForm(forms.ModelForm):
    class Meta:
        model = EmployeeAvailability
        fields = ['start_hour', 'end_hour']




class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'opening_hour', 'closing_hour']



class StoreHoursForm(forms.ModelForm):
    opening_time = forms.ChoiceField(choices=[(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(24)])
    closing_time = forms.ChoiceField(choices=[(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(1, 25)])

    class Meta:
        model = StoreHours
        fields = ['day', 'opening_time', 'closing_time']


''''
class StoreHoursForm(forms.Form):
    DAYS_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day_choices = forms.MultipleChoiceField(choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple)
    opening_hours = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'size': 7}))
    closing_hours = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'size': 7}))

    def __init__(self, *args, **kwargs):
        super(StoreHoursForm, self).__init__(*args, **kwargs)
        hours_choices = [(str(h).zfill(2) + ':00', str(h).zfill(2) + ':00') for h in range(24)]
        self.fields['opening_hours'].choices = hours_choices
        self.fields['closing_hours'].choices = hours_choices
'''


