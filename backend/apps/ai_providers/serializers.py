from rest_framework import serializers

from .models import AIProvider


class AIProviderSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    has_api_key = serializers.SerializerMethodField()

    class Meta:
        model = AIProvider
        fields = [
            'id',
            'public_id',
            'name',
            'scope',
            'base_url',
            'model_name',
            'institute',
            'user',
            'is_active',
            'priority',
            'rate_limit',
            'timeout_seconds',
            'config',
            'has_api_key',
        ]

    def get_has_api_key(self, obj):
        return bool(obj.api_key)


class AIProviderCreateSerializer(serializers.ModelSerializer):
    raw_api_key = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = AIProvider
        fields = [
            'name',
            'scope',
            'raw_api_key',
            'base_url',
            'model_name',
            'institute',
            'user',
            'is_active',
            'priority',
            'rate_limit',
            'timeout_seconds',
            'config',
        ]

    def create(self, validated_data):
        raw_api_key = validated_data.pop('raw_api_key', '')
        provider = AIProvider(**validated_data)
        if raw_api_key:
            provider.encrypt_key(raw_api_key)
        provider.save()
        return provider
