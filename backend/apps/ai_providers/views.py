from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import can_manage_institute, get_primary_institute

from .models import AIProvider
from .serializers import AIProviderCreateSerializer, AIProviderSerializer
from .services import ProviderError, get_adapter, resolve_provider


class AIProviderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AIProviderCreateSerializer
        return AIProviderSerializer

    def get_queryset(self):
        queryset = AIProvider.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        institute_ids = self.request.user.institute_memberships.filter(
            is_active=True,
            role__in=['platform_admin', 'institute_admin'],
        ).values_list('institute_id', flat=True)
        return queryset.filter(user=self.request.user) | queryset.filter(institute_id__in=institute_ids)

    def perform_create(self, serializer):
        scope = serializer.validated_data.get('scope')
        institute = serializer.validated_data.get('institute')
        if scope == 'system' and not (self.request.user.is_staff or self.request.user.is_superuser):
            raise permissions.PermissionDenied('Only platform admins can create system providers.')
        if scope == 'institute' and institute and not can_manage_institute(self.request.user, institute):
            raise permissions.PermissionDenied('You do not manage this institute.')
        serializer.save()


class ProviderHealthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        provider_name = request.query_params.get('provider', 'ollama')
        institute = get_primary_institute(request.user)
        try:
            resolved = resolve_provider(
                provider_name,
                user=request.user,
                institute=institute,
            )
            adapter = get_adapter(
                provider_name,
                user=request.user,
                institute=institute,
            )
            health = adapter.health_check()
            health['scope'] = resolved.scope
            health['model_name'] = resolved.model_name
            return Response(health)
        except ProviderError as exc:
            return Response({'healthy': False, 'provider': provider_name, 'error': str(exc)}, status=404)
