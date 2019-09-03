from .models import License
from django.db.models import F


class LicenseServices():
    def getLicenseByID(self, id):
        return License.objects.get(id=id)

    def getLicenseByLicenseKey(self, license_id):
        return License.objects.get(license_key=license_id)

    def getListLicenseByUser(self, user_id):
        return License.objects.filter(user_id=user_id)
