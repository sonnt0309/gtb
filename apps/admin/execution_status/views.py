from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from apps.admin.activation.models import Activation
from apps.admin.license.models import License
from gtb.utils import Helper, Utils
from rest_framework import status


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