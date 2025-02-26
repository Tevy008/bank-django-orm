from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from datacenter.models import format_time


def get_duration(visit):
    entered_at = timezone.localtime(visit.entered_at)
    now = timezone.localtime(timezone.now())
    delta = now - entered_at
    return delta


def is_visit_long(visit, minutes=60):
    seconds = minutes * 60
    duration = get_duration(visit)
    long_visit = duration.total_seconds() > seconds
    return long_visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in passcard_visits:
        delta = get_duration(visit)
        this_passcard_visits.append({
            'entered_at':
            timezone.localtime(visit.entered_at),
            'duration':
            format_time(delta),
            'is_strange':
            is_visit_long(visit),
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
