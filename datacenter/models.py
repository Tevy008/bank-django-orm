from django.db import models
from datetime import timedelta


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(f'leaved at {self.leaved_at}'
                    if self.leaved_at else 'not leaved'))


def format_time(delta):
    seconds_in_hour = 3600
    minutes_in_hour = 60
    seconds_in_minutes = 60
    seconds = delta.total_seconds()
    hours = seconds // seconds_in_hour
    minutes = (seconds % seconds_in_hour) // minutes_in_hour
    secs = seconds % seconds_in_minutes
    return f'{hours}:{minutes}:{secs}'
