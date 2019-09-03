from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.views.generic import View
from .services import ActivationServices
from .serializers import ActivationSerializer, AcitvationModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from gtb import constant
from gtb.utils import Helper
from helper.hashers import decrypt
import json
from django.utils import translation
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from apps.admin.license.models import License


# Create your views here.
# Custom class for get user by License Id
class ActivationCustomView(LoginRequiredMixin, APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, license_id):
        try:
            license = License.objects.get(license_key=license_id)
        except License.DoesNotExist:
            return Helper.ResponseFormat(status.HTTP_404_NOT_FOUND, '', {})
        data = {
            'user': {
                'name': license.user.profile.full_name_kanji,
                'id': license.user.id
            }
        }
        return Helper.ResponseFormat(status.HTTP_200_OK, '', data)


class ListActivationByLicenseOfUser(generics.ListAPIView):
    activationServices = ActivationServices()

    def get(self, request, user_id):
        try:
            activation = self.activationServices.getListActivationByLicenseOfUser(user_id, request)
            serializer_class = AcitvationModelSerializer(activation, many=True)
        except (ValueError, KeyError) as e:
            return Response({
                'code': 400,
                'message': 'Activation error: %s' % str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('err in ListActivationByLicenseOfUser:', error)
            return Response({
                'code': 500,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'code': 200,
            'data': serializer_class.data,
            'message': 'OKE'
        }, status=status.HTTP_200_OK)


class DetailActivation(generics.RetrieveAPIView):
    activationServices = ActivationServices()

    def get(self, request, id):
        try:
            activation = self.activationServices.getActivationById(id)
            serializer_class = AcitvationModelSerializer(activation)
        except (ObjectDoesNotExist, ValueError):
            return Response({
                'code': 404,
                'message': 'Activation not found'
            }, status= status.HTTP_404_NOT_FOUND)
        except (ValueError, KeyError) as e:
            return Response({
                'code': 400,
                'message': 'Activation error: %s' % str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('err in ListActivationByLicenseOfUser:', error)
            return Response({
                'code': 500,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'code': 200,
            'data': serializer_class.data,
            'message': 'OKE'
        }, status=status.HTTP_200_OK)


class UpdateActivation(generics.UpdateAPIView):
    activationServices = ActivationServices()
    serializer_class = AcitvationModelSerializer
    lookup_field = 'id'

    def put(self, request, id):
        try:
            data = request.data
            license = self.activationServices.getActivationById(id)
            serializer_class = AcitvationModelSerializer(license, data=data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response({
                    'code': 200,
                    'data': serializer_class.data,
                    'message': 'OKE'
                }, status=status.HTTP_200_OK)
            return Response({
                'code': 400,
                'data': serializer_class.errors,
                'message': 'Errors'
            }, status=status.HTTP_400_BAD_REQUEST)
        except (ObjectDoesNotExist, ValueError):
            return Response({
                'code': 404,
                'message': 'Activation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print('err in UpdateActivation:', error)
            return Response({
                'code': 500,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Class handle receive request from client
@csrf_exempt
@api_view(View.http_method_names)
def activateLisence(request):

    # Create response object
    responseData = {
        'activate_status_info' : {
        }
    }

    try:
        # Create activation sevice
        activationService = ActivationServices()
        # Message return client
        message = constant.STR_BLANK

        # setting locale
        # Method handle receive request post from client
        # Object data recive from client
        data = request.data
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


        serializer = ActivationSerializer(data=data)

        if serializer.is_valid() is False:
            return Helper.JsonResponseFormat400(str(request.build_absolute_uri()), 'product_activate', serializer.errors)

        activation = activationService.activeApp(data)

    # In case object license not found in database
    except (ObjectDoesNotExist, ValueError) as error:

        responseData['activate_status_info']['code'] = int(constant.ACTIVATION_FAIL)
        message = str(error)

        # Response for client, activation fail
        return Helper.JsonResponseFormat(status.HTTP_404_NOT_FOUND, message, responseData)
    except Exception as error:

        responseData['activate_status_info']['code'] = int(constant.ACTIVATION_FAIL)
        message = translation.ugettext('Internal error')
        raise
        # Response for client, activation fail
        return Helper.JsonResponseFormat(status.HTTP_500_INTERNAL_SERVER_ERROR, message, responseData)

    # In case License has expired
    if activation.activate_status_code == constant.ACTIVATION_FAIL:
        responseData['activate_status_info']['code'] = int(constant.ACTIVATION_FAIL)
        message = translation.ugettext('License has expired')
    else:
        responseData['activate_status_info']['code'] = int(activation.activate_status_code)
        responseData['activate_status_info']['id'] = activation.activate_key

    # Response for client, activation success
    return Helper.JsonResponseFormat(status.HTTP_200_OK, message, responseData)