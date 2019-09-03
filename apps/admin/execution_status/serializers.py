from rest_framework import serializers
from apps.admin.activation.serializers import ComputerInfoializer
from django.core.validators import MinLengthValidator,MaxLengthValidator,RegexValidator
from gtb import constant
import re


class ActivationSerializer(serializers.Serializer):
    id = serializers.CharField(
        required=True, 
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6),
            RegexValidator(
                regex=re.compile(constant.PATTERN_PATTERN_ALPHANUMERIC),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers'
            )])


class StatusAppSerializer(serializers.Serializer):
    id = serializers.CharField(
        required=True, 
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6),
            RegexValidator(
                regex=re.compile(constant.PATTERN_PATTERN_ALPHANUMERIC),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers'
            )])


class GetStatusAppSerializer(serializers.Serializer):
    activate_status_info = ActivationSerializer(required=True)
    computer_info = ComputerInfoializer(required=True)
    locale = serializers.CharField(required=True)


class UpdateStatusAppSerializer(serializers.Serializer):
    execution_status_id_reflesh =  serializers.BooleanField(default=False)
    execution_status_info = StatusAppSerializer(required=True)
    locale = serializers.CharField(required=True)


class ReleaseStatusAppSerializer(serializers.Serializer):
    execution_status_info = StatusAppSerializer(required=True)
    locale = serializers.CharField(required=True)