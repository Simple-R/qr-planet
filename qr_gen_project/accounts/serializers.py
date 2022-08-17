

from rest_framework import serializers
from qr_generator.models import  QRCollection, UserCollection

from rest_framework import serializers
from accounts.models import QRUser



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length = 6,
        write_only = True
        ) # Make Passwords Readonly so that it wouldn't be sent along with d request


    class Meta:
        model = QRUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return QRUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length = 6,
        write_only = True
        ) # Make Passwords Readonly so that it wouldn't be sent along with d request

    class Meta:
        model = QRUser
        fields = ('email', 'username', 'password', 'token')

        read_only_fields = ['token']


#======================================================
