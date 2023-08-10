from django.db import models


DAY_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    birthday = models.DateField()
    min_working_hours_weekly = models.IntegerField(default=10)
    max_working_hours_weekly = models.IntegerField(default=40)
    
    # Availability fields
    start_monday = models.PositiveIntegerField(default=8, help_text='Start hour for Monday (0-23)')
    end_monday = models.PositiveIntegerField(default=17, help_text='End hour for Monday (0-23)')
    start_tuesday = models.PositiveIntegerField(default=8, help_text='Start hour for Tuesday (0-23)')
    end_tuesday = models.PositiveIntegerField(default=17, help_text='End hour for Tuesday (0-23)')
    start_wednesday = models.PositiveIntegerField(default=8, help_text='Start hour for Wednesday (0-23)')
    end_wednesday = models.PositiveIntegerField(default=17, help_text='End hour for Wednesday (0-23)')
    start_thursday = models.PositiveIntegerField(default=8, help_text='Start hour for Thursday (0-23)')
    end_thursday = models.PositiveIntegerField(default=17, help_text='End hour for Thursday (0-23)')
    start_friday = models.PositiveIntegerField(default=8, help_text='Start hour for Friday (0-23)')
    end_friday = models.PositiveIntegerField(default=17, help_text='End hour for Friday (0-23)')
    start_saturday = models.PositiveIntegerField(default=8, help_text='Start hour for Saturday (0-23)')
    end_saturday = models.PositiveIntegerField(default=17, help_text='End hour for Saturday (0-23)')
    start_sunday = models.PositiveIntegerField(default=8, help_text='Start hour for Sunday (0-23)')
    end_sunday = models.PositiveIntegerField(default=17, help_text='End hour for Sunday (0-23)')

    def __str__(self):
        return self.name



class Store(models.Model):
    name = models.CharField(max_length=100)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()

    def __str__(self):
        return self.name
DAY_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class StoreHours(models.Model):
    day = models.CharField(choices=DAY_CHOICES, max_length=10)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
