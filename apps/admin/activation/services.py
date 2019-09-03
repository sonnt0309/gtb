from .models import Activation
from apps.admin.license.services import LicenseServices
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
from datetime import datetime
import pytz
from gtb import constant
import uuid
from django.utils import translation


# Class handle logic activation
class ActivationServices():
    licenseServices = LicenseServices()

    # Method handle active pc on lisence
    def activeApp(self, data):

        computer_info = data['computer_info']
        try:
            license = self.licenseServices.getLicenseByLicenseKey(data['license_id'])

        # In case object license not found in database
        except (ObjectDoesNotExist, ValueError) as error:
            raise ObjectDoesNotExist(translation.ugettext('License not found'))

        if data['activate_password'] != license.activation_pass and data['activate_password'] != license.user.profile.activation_pass:
            raise ObjectDoesNotExist(translation.ugettext('Activate pass is wrong'))

        # Check Product Name
        if data['application_name'] != license.product.product_name:
            raise ObjectDoesNotExist(translation.ugettext('Product name pass is wrong'))
        # Check PC_Name has exits or not exits
        # In case activation exist on database
        # Get current date
        currentDate = datetime.utcnow().replace(tzinfo=pytz.utc)
        # try:
        #     activation = Activation.objects.get(mac_address=computer_info['mac_address'], license=license)

        #     # In case license expiration bigger current date
        #     if license.license_expiration > currentDate:
        #         activation.activate_status_code=constant.ACTIVATION_SUCCESS
        #     else:
        #         activation.activate_status_code = constant.ACTIVATION_FAIL
        #     activation.save()

        # # In case activation not exist on database
        # except Activation.DoesNotExist:
        # Create object Activation
        activation = Activation();
        activation.activate_key = str(uuid.uuid4())[:6]
        activation.license = license
        activation.pc_name = computer_info['name']
        activation.windows_product_id = computer_info['windows_product_id']
        activation.mac_address = computer_info['mac_address']
        activation.drive_serial_number = computer_info['drive_serial_number']

        # In case license expiration bigger current date
        if license.license_expiration > currentDate:
            activation.activate_status_code = constant.ACTIVATION_SUCCESS
        else:
            activation.activate_status_code = constant.ACTIVATION_FAIL
        # Add activation into database
        activation.save()

        return activation
        
    def getActivationByKey(self, activate_key):
        return Activation.objects.get(
            activate_key = activate_key,
            is_deleted = False,
            activate_status_code = constant.ACTIVATION_SUCCESS)

    def getListActivationByLicenseOfUser(self, user_id, request):
        activation = Activation.objects.filter(license__user__id=user_id)
        if request.GET.get('license_key', False):
            license_key = request.GET.get('license_key')
            activation = activation.filter(license__license_key__icontains=license_key)
        if request.GET.get('product_name', False):
            product_name = request.GET.get('product_name')
            activation = activation.filter(license__product__product_name__icontains=product_name)
        return activation

    def getActivationById(self, id):
        return Activation.objects.get(id=id)
