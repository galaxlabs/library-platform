from django.urls import path

from .views import (
    ClassDarjahDetailView,
    ClassDarjahListView,
    InstituteDetailView,
    InstituteListView,
    InstituteMembershipListView,
    InstitutePrivateLibraryAccessListView,
    InstituteSubjectDetailView,
    InstituteSubjectListView,
)

urlpatterns = [
    path('', InstituteListView.as_view(), name='institute-list'),
    path('<uuid:public_id>/', InstituteDetailView.as_view(), name='institute-detail'),
    path('memberships/', InstituteMembershipListView.as_view(), name='institute-memberships'),
    path('classes/', ClassDarjahListView.as_view(), name='class-darjah-list'),
    path('classes/<uuid:public_id>/', ClassDarjahDetailView.as_view(), name='class-darjah-detail'),
    path('subjects/', InstituteSubjectListView.as_view(), name='institute-subject-list'),
    path('subjects/<uuid:public_id>/', InstituteSubjectDetailView.as_view(), name='institute-subject-detail'),
    path('private-library/', InstitutePrivateLibraryAccessListView.as_view(), name='institute-private-library'),
]
