from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from apps.admin.activation.models import Activation
from apps.admin.license.models import License
from gtb.utils import Helper, Utils
from rest_framework import status
from helper.hashers import decrypt
import json
from gtb import constant
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .serializers import GetStatusAppSerializer, UpdateStatusAppSerializer, ReleaseStatusAppSerializer
from .services import ExecutionStatusServices
from django.db import transaction
from django.utils import translation
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class ExecutionStatusCustomView(LoginRequiredMixin, APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, activate_key):
        try:
            activation = Activation.objects.get(activate_key=activate_key)
        except (Activation.DoesNotExist, License.DoesNotExist):
            return Helper.ResponseFormat(status.HTTP_404_NOT_FOUND, '', {})
        data = {
            'pc_name': activation.pc_name,
            'window_product_id': activation.windows_product_id,
            'mac_address': activation.mac_address,
            'drive_serial_number': activation.drive_serial_number,
            'username': activation.license.user.profile.full_name_kanji,
            'license_id': activation.license.license_key,
            'user_url': activation.license.user.id,
            'license_url': activation.license.id
        }
        return Helper.ResponseFormat(status.HTTP_200_OK, '', data)


# Function handle receive request from client
@csrf_exempt
@api_view(View.http_method_names)
def getStatusApp(request):
    executionStatusServices = ExecutionStatusServices()
    # define response object
    responseData = {
        'execution_status_info': {}
    }

    try:
        # parse request data
        data = request.data
        # setting locale
        language = data.get('locale') or 'en'
        translation.activate(language)

        # check permission api
        decrypt_data = decrypt(data.get('data'))
        if not decrypt_data:
            return Helper.JsonResponseFormat403(str(request.build_absolute_uri()), 'check_permission')
        data = json.loads(decrypt_data)

        # check request method
        if request.method != "POST":
            return Helper.JsonResponseFormat405(str(request.build_absolute_uri()), 'product_activate')

        # check data input
        serializer = GetStatusAppSerializer(data=data)

        if serializer.is_valid() is False:
            return Helper.JsonResponseFormat400(str(request.build_absolute_uri()), 'product_activate',
                                                serializer.errors)

        # if exception occur then it will be rollback
        with transaction.atomic():

            # execute logic
            executionStatus, message, operationSetting = executionStatusServices.getStatusApp(data)

            # create object to return
            if executionStatus.status_code == constant.APP_EXE_STATUS_SUCCESS:
                license = executionStatus.activation.license
                product = license.product
                licensed_options = []
                latest_versions = []
                oldest_versions = []

                # get option and convert Object to array
                for opt in license.option.all():
                    licensed_options.append(opt.option_name)

                if operationSetting.latest_version:
                    latest_versions = list(map(lambda x: int(x) or 0, operationSetting.latest_version.split('.')))

                if operationSetting.oldest_version:
                    oldest_versions = list(map(lambda x: int(x) or 0, operationSetting.oldest_version.split('.')))

                responseData['license_expiration'] = Utils.datetimeTOTimestamp(license.license_expiration)
                responseData['execution_status_info']['id'] = executionStatus.app_exe_status_key
                responseData['execution_status_info']['code'] = int(executionStatus.status_code)
                responseData['execution_status_info']['expiration'] = Utils.datetimeTOTimestamp(
                    executionStatus.exe_status_expiration)
                responseData['execution_status_check_interval_seconds'] = operationSetting.check_interval_seconds
                responseData['licensed_options'] = ','.join(licensed_options)
                responseData['support_client_version_info'] = {}
                responseData['support_client_version_info']['latest'] = latest_versions
                responseData['support_client_version_info']['oldest'] = oldest_versions
                # responseData['message'] = message
            else:
                responseData['execution_status_info']['code'] = int(executionStatus.status_code)
                responseData['message'] = message

    except (ObjectDoesNotExist, ValueError) as error:
        responseData['execution_status_info']['code'] = int(constant.APP_EXE_STATUS_FAIL)
        responseData['message'] = str(error)

    except Exception as error:
        print(error)
        responseData['execution_status_info']['code'] = int(constant.APP_EXE_STATUS_FAIL)
        responseData['message'] = translation.ugettext('Internal error')
    print(responseData)
    return Helper.JsonResponseFormat(status.HTTP_200_OK, constant.STR_BLANK, responseData)


# Function handle receive request from client
@csrf_exempt
@api_view(View.http_method_names)
def updateStatusApp(request):
    executionStatusServices = ExecutionStatusServices()
    # define response object
    responseData = {
        'execution_status_info': {}
    }

    try:
        # parse request data
        data = request.data
        # setting locale
        language = data.get('locale') or 'en'
        translation.activate(language)

        decrypt_data = decrypt(data.get('data'))
        if not decrypt_data:
            return Helper.JsonResponseFormat403(str(request.build_absolute_uri()), 'check_permission')
        data = json.loads(decrypt_data)

        # check request method
        if request.method != "POST":
            return Helper.JsonResponseFormat405(str(request.build_absolute_uri()), 'product_activate')

        # check data input
        serializer = UpdateStatusAppSerializer(data=data)
        if serializer.is_valid() is False:
            return Helper.JsonResponseFormat400(str(request.build_absolute_uri()), 'product_activate',
                                                serializer.errors)

        # if exception occur then it will be rollback
        with transaction.atomic():
            # execute logic
            executionStatus, message, operationSetting = executionStatusServices.updateStatusApp(data)

            # create object to return
            if executionStatus.status_code == constant.APP_EXE_STATUS_SUCCESS:

                license = executionStatus.activation.license
                product = license.product

                licensed_options = []
                latest_versions = []
                oldest_versions = []

                # get option and convert Object to array
                for opt in license.option.all():
                    licensed_options.append(opt.option_name)

                if operationSetting.latest_version:
                    latest_versions = list(map(lambda x: int(x) or 0, operationSetting.latest_version.split('.')))

                if operationSetting.oldest_version:
                    oldest_versions = list(map(lambda x: int(x) or 0, operationSetting.oldest_version.split('.')))

                responseData['license_expiration'] = Utils.datetimeTOTimestamp(license.license_expiration)
                responseData['execution_status_info']['id'] = executionStatus.app_exe_status_key
                responseData['execution_status_info']['code'] = int(executionStatus.status_code)
                responseData['execution_status_info']['expiration'] = Utils.datetimeTOTimestamp(
                    executionStatus.exe_status_expiration)
                responseData['execution_status_check_interval_seconds'] = operationSetting.check_interval_seconds
                responseData['licensed_options'] = ','.join(licensed_options)
                responseData['support_client_version_info'] = {}
                responseData['support_client_version_info']['latest'] = latest_versions
                responseData['support_client_version_info']['oldest'] = oldest_versions
                # responseData['message'] = message
            else:
                responseData['execution_status_info']['code'] = int(executionStatus.status_code)
                responseData['message'] = message

    except (ObjectDoesNotExist, ValueError) as error:
        responseData['execution_status_info']['code'] = int(constant.APP_EXE_STATUS_FAIL)
        responseData['message'] = str(error)

    except Exception as error:
        print(error)
        responseData['execution_status_info']['code'] = int(constant.APP_EXE_STATUS_FAIL)
        responseData['message'] = translation.ugettext('Internal error')
    print(responseData)
    return Helper.JsonResponseFormat(status.HTTP_200_OK, constant.STR_BLANK, responseData)


# function handle receive request post from client
@csrf_exempt
@api_view(View.http_method_names)
def releaseStatusApp(request):
    # Create service execution status
    executionStatusServices = ExecutionStatusServices()

    # Create response object
    responseData = {
        'release_status_info': {
        }
    }
    try:
        # parse request data
        data = request.data
        language = data.get('locale') or 'en'
        translation.activate(language)

        decrypt_data = decrypt(data.get('data'))
        if not decrypt_data:
            return Helper.JsonResponseFormat403(str(request.build_absolute_uri()), 'check_permission')
        data = json.loads(decrypt_data)

        # check request method
        if request.method != "POST":
            return Helper.JsonResponseFormat405(str(request.build_absolute_uri()), 'product_activate')

        # Message return client
        message = constant.STR_BLANK
        # Language receive from client
        # Active language receive from client, get message with that language

        serializer = ReleaseStatusAppSerializer(data=data)
        if serializer.is_valid() is False:
            return Helper.JsonResponseFormat400(str(request.build_absolute_uri()), 'product_activate',
                                                serializer.errors)

        executionStatus = executionStatusServices.releaseApp(data)

    # In case object execution status not found in database
    except (ObjectDoesNotExist, ValueError) as error:
        message = translation.ugettext(str(error))
        responseData['release_status_info']['code'] = int(constant.RELEASE_FAIL)

        # Response for client, release status fail
        return Helper.JsonResponseFormat(status.HTTP_404_NOT_FOUND, message, responseData)
    except Exception as error:
        message = translation.ugettext('Internal error')
        responseData['release_status_info']['code'] = int(constant.RELEASE_FAIL)
        # Response for client, release status fail
        return Helper.JsonResponseFormat(status.HTTP_500_INTERNAL_SERVER_ERROR, message, responseData)

    # Release Execution status success
    responseData['release_status_info']['code'] = int(executionStatus.status_code)

    # Response for client, release status success
    return Helper.JsonResponseFormat(status.HTTP_200_OK, message, responseData)