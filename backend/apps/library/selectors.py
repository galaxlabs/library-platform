from django.db.models import Q

from apps.common.permissions import has_institute_role
from apps.institutes.models import InstitutePrivateLibraryAccess

from .models import Book, BookChunk


def visible_books_queryset(user):
    queryset = Book.objects.select_related('primary_subject', 'uploaded_by', 'institute').prefetch_related(
        'files',
        'skill_packs',
    )
    if not user or not user.is_authenticated:
        return queryset.filter(visibility='public', public=True)

    institute_ids = list(
        user.institute_memberships.filter(is_active=True).values_list('institute_id', flat=True)
    )
    accessible_private_ids = list(
        InstitutePrivateLibraryAccess.objects.filter(
            is_active=True,
            institute_id__in=institute_ids,
        ).values_list('book_id', flat=True)
    )

    return queryset.filter(
        Q(visibility='public', public=True)
        | Q(uploaded_by=user)
        | Q(institute_id__in=institute_ids)
        | Q(id__in=accessible_private_ids)
        | Q(institute__admin=user)
    ).distinct()


def visible_chunks_queryset(user):
    return BookChunk.objects.select_related('book', 'book_file').filter(
        book_id__in=visible_books_queryset(user).values('id')
    )
