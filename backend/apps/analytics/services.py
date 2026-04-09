from .models import EventLog


def track_event(name: str, *, user=None, payload=None):
    return EventLog.objects.create(name=name, user=user, payload=payload or {})
