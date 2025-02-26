from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone
from datacenter.models import format_time


def storage_information_view(request):
    leaved_at_visit = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in leaved_at_visit:
        non_closed_visits.append({
            'who_entered':
            visit.passcard.owner_name,
            'entered_at':
            timezone.localtime(visit.entered_at),
            'duration':
            format_time(timezone.now() - visit.entered_at),
        })
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
