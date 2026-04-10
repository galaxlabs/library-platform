from django.db.models import Count, Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import can_access_institute, can_manage_institute

from .models import (
    ClassDarjah,
    Institute,
    InstituteMembership,
    InstitutePrivateLibraryAccess,
    InstituteSubject,
)
from .serializers import (
    ClassDarjahSerializer,
    InstituteMembershipSerializer,
    InstitutePrivateLibraryAccessSerializer,
    InstituteSerializer,
    InstituteSubjectSerializer,
)


class InstituteScopedMixin:
    permission_classes = [IsAuthenticated]

    def _requested_institute_id(self):
        return self.request.query_params.get('institute')

    def _user_institutes(self):
        return Institute.objects.filter(
            Q(memberships__user=self.request.user, memberships__is_active=True)
            | Q(admin=self.request.user)
        ).distinct()

    def _visible_institutes(self):
        queryset = Institute.objects.filter(is_active=True).annotate(
            memberships_count=Count('memberships', filter=Q(memberships__is_active=True))
        )
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(
            Q(id__in=self._user_institutes().values('id'))
            | Q(books__visibility='public', books__public=True)
        ).distinct()


class InstituteListView(InstituteScopedMixin, generics.ListAPIView):
    serializer_class = InstituteSerializer

    def get_queryset(self):
        return self._visible_institutes()


class InstituteDetailView(InstituteScopedMixin, generics.RetrieveAPIView):
    serializer_class = InstituteSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        return self._visible_institutes()


class InstituteMembershipListView(InstituteScopedMixin, generics.ListAPIView):
    serializer_class = InstituteMembershipSerializer

    def get_queryset(self):
        queryset = InstituteMembership.objects.filter(is_active=True).select_related(
            'user',
            'institute',
            'class_darjah',
        )
        institute_id = self._requested_institute_id()
        if institute_id:
            queryset = queryset.filter(institute__public_id=institute_id)

        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset

        if institute_id:
            institute = Institute.objects.filter(public_id=institute_id).first()
            if institute and can_manage_institute(self.request.user, institute):
                return queryset

        return queryset.filter(user=self.request.user)


class ClassDarjahListView(InstituteScopedMixin, generics.ListAPIView):
    serializer_class = ClassDarjahSerializer

    def get_queryset(self):
        queryset = ClassDarjah.objects.select_related('institute')
        institute_id = self._requested_institute_id()
        if institute_id:
            queryset = queryset.filter(institute__public_id=institute_id)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(institute_id__in=self._visible_institutes().values('id')).distinct()


class ClassDarjahDetailView(InstituteScopedMixin, generics.RetrieveAPIView):
    serializer_class = ClassDarjahSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        queryset = ClassDarjah.objects.select_related('institute')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(institute_id__in=self._visible_institutes().values('id'))


class InstituteSubjectListView(InstituteScopedMixin, generics.ListAPIView):
    serializer_class = InstituteSubjectSerializer

    def get_queryset(self):
        queryset = InstituteSubject.objects.select_related('institute', 'subject', 'class_darjah')
        institute_id = self._requested_institute_id()
        if institute_id:
            queryset = queryset.filter(institute__public_id=institute_id)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(institute_id__in=self._visible_institutes().values('id')).distinct()


class InstituteSubjectDetailView(InstituteScopedMixin, generics.RetrieveAPIView):
    serializer_class = InstituteSubjectSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        queryset = InstituteSubject.objects.select_related('institute', 'subject', 'class_darjah')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(institute_id__in=self._visible_institutes().values('id'))


class InstitutePrivateLibraryAccessListView(InstituteScopedMixin, generics.ListAPIView):
    serializer_class = InstitutePrivateLibraryAccessSerializer

    def get_queryset(self):
        queryset = InstitutePrivateLibraryAccess.objects.filter(is_active=True).select_related(
            'institute',
            'book',
        )
        institute_id = self._requested_institute_id()
        if institute_id:
            queryset = queryset.filter(institute__public_id=institute_id)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(institute_id__in=self._user_institutes().values('id')).distinct()
