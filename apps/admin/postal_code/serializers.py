from rest_framework import serializers
from .models import PostalCode


class PostTalCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostalCode
        fields = ['id', 'zip', 'ken_id', 'city_id', 'town_id', 'office_flg', 'delete_flg', 'ken_name', 'ken_furi', 'city_name',
        'city_furi', 'town_name', 'town_furi', 'town_memo', 'kyoto_street', 'block_name', 'block_furi', 'memo',
        'office_furi', 'office_address', 'new_id']