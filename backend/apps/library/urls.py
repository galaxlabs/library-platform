from django.urls import path

from .views import (
    BookChunkListView,
    BookDetailView,
    BookFileListView,
    BookListCreateView,
    BookReferenceListView,
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<uuid:public_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<uuid:public_id>/files/', BookFileListView.as_view(), name='book-files'),
    path('books/<uuid:public_id>/chunks/', BookChunkListView.as_view(), name='book-chunks'),
    path('books/<uuid:public_id>/references/', BookReferenceListView.as_view(), name='book-references'),
]
