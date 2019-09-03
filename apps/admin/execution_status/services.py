from .models import ExecutionStatus
from django.db.models import F
from apps.admin.license.models import License
from apps.admin.activation.services import ActivationServices
from apps.admin.operation_setting.services import OperationSettingServices
from django.core.exceptions import ObjectDoesNotExist
from gtb import constant
from datetime import datetime, timezone, timedelta
from django.utils import translation
from django.db import transaction, IntegrityError
import pytz, uuid


# Class handle logic execution status
class ExecutionStatusServices():

    activationServices = ActivationServices()
    operationSettingServices = OperationSettingServices()

    # Get info execution status by app_exe_status_key
    def getExecutionStatusByExecutionStatusKey(self, app_exe_status_key):
        return ExecutionStatus.objects.get(app_exe_status_key = app_exe_status_key, is_deleted = False)

    def getNumberOfActiveStatusApp(self, license, currentDate):
        exe = ExecutionStatus.objects.filter(
            exe_status_expiration__gte = currentDate,
            activation__is_deleted = False,
            activation__activate_status_code = constant.ACTIVATION_SUCCESS,
            activation__license = license,
            status_code = constant.APP_EXE_STATUS_SUCCESS,
            is_deleted = False
        )
        return exe

    def getExecutionStatusByActivation(self, activation, currentDate):
        return ExecutionStatus.objects.filter(
            exe_status_expiration__gte = currentDate,
            activation = activation,
            status_code = constant.APP_EXE_STATUS_SUCCESS,
            is_deleted = False
        )

    # サーバへ実行ステータスの新規作成と、関連情報を要求する
    def getStatusApp(self, data):

        language = data.get('locale') or 'en'
        translation.activate(language)

        status_code = constant.APP_EXE_STATUS_FAIL
        message = ''
        operationSetting = None
        computer_info = data['computer_info']

        # Get activation to check
        try:
            activation = self.activationServices.getActivationByKey(data['activate_status_info']['id'])
        except (ObjectDoesNotExist, ValueError) as error:
            print(translation.ugettext('Activation not found'))
            raise ObjectDoesNotExist(translation.ugettext('Activation not found'))

        # Check expirate of license
        currentDate = datetime.utcnow().replace(tzinfo=pytz.utc)
        exe_status_expiration = datetime(1900, 1, 1, tzinfo=timezone.utc)

        exe_temp = self.getExecutionStatusByActivation(activation, currentDate)
        if len(exe_temp) > 0:
            raise ObjectDoesNotExist(translation.ugettext('Activation has been used'))

        license = activation.license
        # Check license is delete
        if license is None or license.is_deleted is True or license.pause is True:
            raise ObjectDoesNotExist(translation.ugettext('License not found or paused'))

        # Check the license and the licenses access
        if license.license_expiration > currentDate:

            list_status_app = self.getNumberOfActiveStatusApp(license, currentDate)

            if (len(list_status_app) < (license.start_app_num or 0)):

                # check MAC_ADDRESS
                countErr = 0
                fieldErr = []
                if activation.pc_name != data['computer_info']['name']:
                    countErr += 1
                    fieldErr.append(translation.ugettext('pc name'))
                if activation.windows_product_id != data['computer_info']['windows_product_id']:
                    countErr += 1
                    fieldErr.append(translation.ugettext('windows product ID'))
                if activation.mac_address != data['computer_info']['mac_address']:
                    countErr += 1
                    fieldErr.append(translation.ugettext('mac address'))
                if activation.drive_serial_number != data['computer_info']['drive_serial_number']:
                    countErr += 1
                    fieldErr.append(translation.ugettext('drive serial number'))

                # If the 3 fields match, it will be successful 
                if countErr < 3:
                    # set status
                    status_code = constant.APP_EXE_STATUS_SUCCESS
                    # return success
                    message = translation.ugettext('Start the application successfully')
                    # get operationSetting of product
                    operationSetting = self.operationSettingServices.getOperationSettingByProduct(license.product)
                    if operationSetting is None:
                        raise ObjectDoesNotExist(translation.ugettext('OperationSetting not found'))

                    exe_status_expiration = currentDate + timedelta(seconds=(operationSetting.status_valid_seconds or 0))

                else:
                    message = (translation.ugettext("The {} is not used correctly with the registered one at Activation")).format(','.join(fieldErr))
            else:
                message = translation.ugettext('The number of license is limited')
                print(message)
        else:
            message = translation.ugettext('The license of products is expired')

        # Insert always execute 
        executionStatus = ExecutionStatus.objects.create_status(
                activation=activation,
                app_exe_status_key=str(uuid.uuid4())[:6],
                status_code=status_code,
                exe_status_expiration=exe_status_expiration
            )
        return executionStatus,message,operationSetting

    # サーバへIDで示される実行ステータスの更新を要求する
    def updateStatusApp(self, data):

        # get locale from request and use to return message for client
        language = data.get('locale') or 'en'
        translation.activate(language)

        # set status
        status_code = constant.APP_EXE_STATUS_FAIL
        message = ''
        operationSetting = None
        currentDate = datetime.utcnow().replace(tzinfo=pytz.utc)
        # default exe_status_expiration
        exe_status_expiration = datetime(1900, 1, 1, tzinfo=timezone.utc)

        # Get Execution status to check
        try:
            executionStatus = self.getExecutionStatusByExecutionStatusKey(data['execution_status_info']['id'])

        except (ObjectDoesNotExist, ValueError) as error:
            raise ObjectDoesNotExist(translation.ugettext('Execution status not found'))

        if executionStatus.status_code == constant.APP_EXE_STATUS_FAIL:
            raise ObjectDoesNotExist(translation.ugettext('Execution status do not activate.'))

        if executionStatus.status_code == constant.RELEASE_SUCCESS :
            raise ObjectDoesNotExist(translation.ugettext('Execution status can not be updated because the application ended.'))

        # Check EXE_STATUS_EXPIRATION is active
        if executionStatus.exe_status_expiration < currentDate:
            raise ObjectDoesNotExist(translation.ugettext('Execution status is expired'))
        
        # get license
        license = executionStatus.activation.license

        # Check license is delete
        if license is None or license.is_deleted is True or license.pause is True:
            raise ObjectDoesNotExist(translation.ugettext('License not found or paused'))

        # Check the expired license 
        if license.license_expiration > currentDate:

            # if the number of starting App <= the number of limit then App is accessed
            list_status_app = self.getNumberOfActiveStatusApp(license, currentDate)

            if (len(list_status_app) <= (license.start_app_num or 0)):

                status_code = constant.APP_EXE_STATUS_SUCCESS
                message = translation.ugettext('Update the application successfully')

                # get operationSetting of product
                operationSetting = self.operationSettingServices.getOperationSettingByProduct(license.product)
                if operationSetting is None:
                    raise ObjectDoesNotExist(translation.ugettext('OperationSetting status not found'))

                exe_status_expiration = currentDate + timedelta(seconds=(operationSetting.status_valid_seconds or 0))

            else:
                message = translation.ugettext('The number of license is limited')
        else:
            message = translation.ugettext('The license of products is expired')

        # update app_exe_status
        if data['execution_status_id_reflesh'] == True:
            executionStatus.app_exe_status_key = str(uuid.uuid4())[:6]
            executionStatus.exe_status_expiration=exe_status_expiration
            executionStatus.status_code=status_code
        else:
            # executionStatus.exe_status_expiration=exe_status_expiration
            executionStatus.status_code=status_code

        print(exe_status_expiration)
        executionStatus.save()

        return executionStatus,message,operationSetting
    
    # Method handle release execution status
    def releaseApp(self, data):
        execution_status_info = data['execution_status_info']
        try:
            executionStatus = self.getExecutionStatusByExecutionStatusKey(execution_status_info['id'])

        # In case object execution status not found in database
        except (ObjectDoesNotExist, ValueError) as error:
            raise ObjectDoesNotExist('Execution status not found')

        if executionStatus.status_code == constant.RELEASE_SUCCESS:
            raise ObjectDoesNotExist('Execution status can not be updated because the application ended.')
            
        try:
            # Manage transaction
            with transaction.atomic():
                # Update execution status
                executionStatus.status_code = constant.RELEASE_SUCCESS
                executionStatus.save()
        except IntegrityError:
            raise

        return executionStatus
