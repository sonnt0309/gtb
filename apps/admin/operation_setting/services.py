from .models import OperationSetting

class OperationSettingServices():
    def getOperationSettingByProduct(self, product):
        return OperationSetting.objects.filter(product=product).order_by('-created_date').first()
