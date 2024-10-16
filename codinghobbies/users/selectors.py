from django.db.models import QuerySet
from .models import Profile


def get_profile(*, user: str) -> Profile:
    return Profile.objects.get(user=user)
