from rest_framework import serializers
from django.core.validators import RegexValidator
import re
from django.core.validators import MinLengthValidator,MaxLengthValidator
from helper.validate import validate_activation_pass
from gtb import constant
from .models import Activation


class ComputerInfoializer(serializers.Serializer):
    name = serializers.CharField(required=True, validators=[MaxLengthValidator(150)])
    windows_product_id = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(24),
            RegexValidator(
                regex=re.compile(constant.PATTERN_WINDOWS_PRODUCT_ID),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers,hyphen'
            )
        ])
    mac_address = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(20),
            RegexValidator(
                regex=re.compile(constant.PATTERN_MAC_ADDRESS),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers,hyphen'
            )
    ])
    drive_serial_number = serializers.CharField(
        required=True,
        validators=[
            MaxLengthValidator(20),
            RegexValidator(
                regex=re.compile(constant.PATTERN_DRIVE_SERIAL_NUMBER),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers,hyphen'
            )
    ])


class ActivationSerializer(serializers.Serializer):
    license_id = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6),
            RegexValidator(
                regex=re.compile(constant.PATTERN_PATTERN_ALPHANUMERIC),
                code=constant.INVALID_FORMAT_CODE,
                message='includes alphabet and numbers'
            )
        ]
       )
    application_name = serializers.CharField(required=True)
    activate_password = serializers.CharField(validators=[MaxLengthValidator(128), validate_activation_pass], required=True)
    computer_info = ComputerInfoializer(required=True)
    locale = serializers.CharField(required=True)


class AcitvationModelSerializer(serializers.ModelSerializer):
    license_key = serializers.StringRelatedField(source='license')
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Activation
        exclude = ('is_deleted',)

    def get_product_name(self, obj):
        return obj.license.product.product_name
