from rest_framework.serializers import ModelSerializer
from qr_generator.models import QRCollection


class QRCollectionSerializer(ModelSerializer):
    class Meta:
        model = QRCollection
        fields = ('id','category','qr_code','qr_info','time_created')
        