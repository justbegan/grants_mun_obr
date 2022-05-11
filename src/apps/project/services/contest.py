from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from apps.contest.models import Contest, Direction

"""
    
"""
def get_open_contest():
    try:
        # не новые(NEW) конкурсы
        contests = Contest.objects.all().filter(~Q(status=Contest.NEW))

        # если последний - активный (предполагается)
        contest = contests.last()
        
    except ObjectDoesNotExist:
        contest = False

    return contest


def get_contest_directions(id):
    return Direction.objects.all()