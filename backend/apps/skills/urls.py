from django.urls import path

from .views import SkillPackDetailView, SkillPackListView

urlpatterns = [
    path('packs/', SkillPackListView.as_view(), name='skill-pack-list'),
    path('packs/<uuid:public_id>/', SkillPackDetailView.as_view(), name='skill-pack-detail'),
]
