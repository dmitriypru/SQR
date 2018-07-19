from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import UserAction
from datetime import datetime
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'secret_word', 'school_name', 'school_klass', 'school_klass_litera')

class UserRegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = get_user_model().objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
        )
        user.school_klass = '8'
        user.school_klass_litera = 'Е'
        user.set_password(validated_data['password'])
        user.school_name = 'ЦНТТ "Информатика+"'
        user.secret_word = pyotp.random_base32()
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'password': {'write_only': True},
            'username': {'write_only': True}
        }

class ActionSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=6)
    secret_word = serializers.CharField(max_length=25)
    is_come_in = serializers.BooleanField()

    def validate(self, data):
        if not get_user_model().objects.filter(secret_word=data['secret_word']).exists():
            raise CustomValidation('User does not exist', 'secret_word', status_code=status.HTTP_409_CONFLICT)
        elif pyotp.TOTP(get_user_model().objects.get(secret_word=data['secret_word']).secret_word, interval=30).now() != data['code']:
            raise CustomValidation('Code does not right', 'code', status_code=status.HTTP_409_CONFLICT)
        return data

    def create(self, validated_data):
        action = UserAction.objects.create(
            user=get_user_model().objects.get(secret_word=validated_data['secret_word']),
            is_come_in=validated_data['is_come_in'],
        )
        return action


class CustomValidation(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}
