from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    public_id = serializers.UUIDField(read_only=True)
    institute_name = serializers.CharField(source='institute.name', read_only=True)
    class_darjah_name = serializers.CharField(source='class_darjah.name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'public_id',
            'email',
            'full_name',
            'arabic_name',
            'phone',
            'roles',
            'preferred_lang_pair',
            'institute',
            'institute_name',
            'class_darjah',
            'class_darjah_name',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'arabic_name',
            'phone',
            'preferred_lang_pair',
            'password',
            'password_confirm',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        email = validated_data['email']
        user = User.objects.create_user(username=email, **validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Email and password required.')

        attrs['user'] = user
        return attrs


class MeSerializer(UserSerializer):
    membership_roles = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['membership_roles']

    def get_membership_roles(self, obj):
        return list(
            obj.institute_memberships.filter(is_active=True).values_list('role', flat=True).distinct()
        )
