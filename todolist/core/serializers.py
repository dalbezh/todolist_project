from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        if attrs["password"] != attrs["password_repeat"]:
            msg = _('Пароль не совпадает.')
            raise ValidationError(detail=msg, code="registration")
        if validate_password(password=attrs["password"]) is not None:
            raise ValidationError()
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = attrs["user"]
        if not user.check_password(attrs["old_password"]):
            msg = _("Некорректный текущий пароль.")
            raise ValidationError(detail=msg, code="update")
        if attrs["old_password"] == attrs["new_password"]:
            msg = _("Новый пароль не должен быть идентичен старому.")
            raise ValidationError(detail=msg, code="update")
        if validate_password(password=attrs["new_password"], user=user) is not None:
            raise ValidationError()
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data["new_password"])
        instance.save(update_fields=("password",))
        return instance
