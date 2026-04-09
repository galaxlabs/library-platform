from django.urls import path

from .views import KnowledgeObjectDetailView, KnowledgeObjectListView, TopicMapListView

urlpatterns = [
    path('objects/', KnowledgeObjectListView.as_view(), name='knowledge-object-list'),
    path('objects/<uuid:public_id>/', KnowledgeObjectDetailView.as_view(), name='knowledge-object-detail'),
    path('topics/', TopicMapListView.as_view(), name='knowledge-topic-map'),
]
