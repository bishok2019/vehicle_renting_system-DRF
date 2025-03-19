from rest_framework import serializers
from .models import Profile, User, Department
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from role_app.models import Role

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    # department = serializers.CharField(source='visiting_to.department.name', read_only=True)
    depart = serializers.CharField(source='department.name', read_only=True)

    action = serializers.SerializerMethodField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True, write_only=True,many=True)

    #this willnot work because it expect single role but its have manytomany relation with user
    # action = serializers.CharField(source='role.name', default="", read_only=True)

    class Meta:
        model = User
        fields = ['id','username','department','email','role','is_active','action','depart']
        read_only_fields = ['id', 'username']

    def get_action(self, obj):
        roles = obj.role.all()
        return ", ".join(role.name for role in roles) or None
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'is_email_verified', 'profile_image')
        read_only_fields = ('is_email_verified',)

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password.')
            if not hasattr(user, 'profile'):
                raise serializers.ValidationError('No Profile for this current user.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            if not user.profile.is_email_verified:
                raise serializers.ValidationError('Email is not verified.')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Must include "username" and "password".')

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('No user found with this email address.')
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid token or user ID.')

        if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid or expired token.')

        attrs['user'] = user
        return attrs

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance