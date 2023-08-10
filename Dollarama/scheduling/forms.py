from django import forms
from django.forms import inlineformset_factory
from .models import Employee,Store,StoreHours,DAY_CHOICES

# forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name',
            'phone_number',
            'birthday',
            'min_working_hours_weekly',
            'max_working_hours_weekly',
            'start_monday',
            'end_monday',
            'start_tuesday',
            'end_tuesday',
            'start_wednesday',
            'end_wednesday',
            'start_thursday',
            'end_thursday',
            'start_friday',
            'end_friday',
            'start_saturday',
            'end_saturday',
            'start_sunday',
            'end_sunday',
        ]


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


