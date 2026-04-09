from django.urls import path

from .views import DashboardCountersView

urlpatterns = [
    path('dashboard/', DashboardCountersView.as_view(), name='analytics-dashboard'),
]
