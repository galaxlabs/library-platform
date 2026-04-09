from django.urls import path

from .views import ChatView, QuestionDetailView, QuestionListCreateView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='qa-question-list'),
    path('questions/<uuid:public_id>/', QuestionDetailView.as_view(), name='qa-question-detail'),
    path('chat/', ChatView.as_view(), name='qa-chat'),
]
