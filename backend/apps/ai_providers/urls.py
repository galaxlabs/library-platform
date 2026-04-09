from django.urls import path

from .views import AIProviderListCreateView, ProviderHealthView

urlpatterns = [
    path('', AIProviderListCreateView.as_view(), name='provider-list'),
    path('health/', ProviderHealthView.as_view(), name='provider-health'),
]
