from django.core.management.base import BaseCommand
from django.utils import timezone
from advanced_filters.models import AdvancedFilter
from apps.admin.user.models import User


class Command(BaseCommand):
    help = 'create seed data advanced filter'

    def handle(self, *args, **kwargs):
        create_user = User.objects.create_user(id=-1, username='data_advanced_filter',
                                               email='data_advanced_filter@gmail.com', password=123456)
        create_user.is_active = False
        create_user.is_deleted = True
        create_user.save()
        advancedFilter = AdvancedFilter.objects.filter(id=1)
        if len(advancedFilter) == 0:
            AdvancedFilter.objects.create(
                id=1, title='', url='',
              b64_query='eyJjaGlsZHJlbiI6IFtbInByb2ZpbGVfX2NyZWF0ZWRfZGF0ZV9faWV4YWN0IiwgIjIwMTktMDUtMDEiXV0sICJjb25uZWN0b3IiOiAiQU5EIiwgIm5lZ2F0ZWQiOiBmYWxzZX0=',
              model='user.User', created_by_id=-1
            )
            AdvancedFilter.objects.filter(id=1).update(created_at='2000-06-20 07:55:24.000000')
            self.stdout.write(self.style.SUCCESS('Create data advanced filter success!'))
        AdvancedFilter.objects.filter(id=1).update(title='', created_at='2000-06-20 07:55:24.000000', created_by_id=-1)
        self.stdout.write(self.style.SUCCESS('Create data advanced filter success!'))
