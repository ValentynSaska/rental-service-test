from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'login', 'first_name', 'last_name', 'phone_number', 'date_joined']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    login = serializers.CharField()
    password = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['login'] = user.login
        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('login')
        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'login', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            login=validated_data['login'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            is_staff=False,
            is_superuser=False,
        )
        return user
