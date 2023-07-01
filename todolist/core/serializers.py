from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.exceptions import AuthenticationFailedRu, PasswordDontMatch, IncorrectPassword, IdenticalPassword

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = authenticate(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        if not user:
            raise AuthenticationFailedRu
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Принимает password и password_repeat
    и проверять, совпадают ли они;
    """
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    password_repeat = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs):
        """
        метод validate_password() - проверяет пароль на соответствие с настройками
        указанными в settings.py (AUTH_PASSWORD_VALIDATORS)
        """
        if attrs["password"] != attrs["password_repeat"]:
            raise PasswordDontMatch
        if validate_password(password=attrs["password"]) is not None:
            raise ValidationError()
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для обновления пароля
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = attrs["user"]
        if not user.check_password(attrs["old_password"]):
            raise IncorrectPassword
        if attrs["old_password"] == attrs["new_password"]:
            raise IdenticalPassword
        if validate_password(password=attrs["new_password"], user=user) is not None:
            raise ValidationError()
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data["new_password"])
        instance.save(update_fields=("password",))
        return instance
