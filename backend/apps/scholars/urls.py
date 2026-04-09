from django.urls import path

from .views import ScholarApplicationView, ScholarProfileView, ScholarReviewListCreateView

urlpatterns = [
    path('me/', ScholarProfileView.as_view(), name='scholar-profile'),
    path('applications/', ScholarApplicationView.as_view(), name='scholar-application'),
    path('reviews/', ScholarReviewListCreateView.as_view(), name='scholar-reviews'),
]
