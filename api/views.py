from unicodedata import category
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from qr_gen_project.accounts import LoginSerializer, RegisterSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from qr_generator.models import QRCollection

from qr_generator.serializers import QRCollectionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView


#==========================================
class AuthUserAPIView(GenericAPIView):
    """This Fetches the Available User **(User Must be logged in first)"""

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self, request):
        user = request.user
        serializer = RegisterSerializer(user)

        return response.Response({'user':serializer.data})

class RegisterAPIView(GenericAPIView):
    """This Registers a New User to use the APIs """
    authentication_classes = []
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    """This Logs a Registered User in **(Requires Authentication Token)"""
    authentication_classes = []
    
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)
     

        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({"message":"invalid creadentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)

#=========================================================

class QRAPIView(ListAPIView):
    """This fetches All User QRs availale, **(User Must be logged in first)"""
    serializer_class = QRCollectionSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self):
        return QRCollection.objects.filter(qr_user=self.request.user, )


class QRDetailAPIView(RetrieveAPIView):
    serializer_class = QRCollectionSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self):
        

        return QRCollection.objects.filter(qr_user=self.request.user, )

class QRCategoryView(ListAPIView):
    """All User QR from a specified Category"""
    serializer_class = QRCollectionSerializer
    permission_classes =(IsAuthenticated,)

    
    def get_queryset(self):

        if self.kwargs['category']:
            try:
                qr = QRCollection.objects.filter(
                qr_user=self.request.user,
                category=self.kwargs['category'],
                )
            except TypeError as ex:
                return {'message':"error"}

            return qr

class DeleteQRAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QRCollectionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return QRCollection.objects.filter(
            qr_user=self.request.user
        )
        
    
class QROneCategoryView(RetrieveDestroyAPIView):
    serializer_class = QRCollectionSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self):

        if self.kwargs['category']:
            if self.kwargs['pk']:
                try:
                    qr = QRCollection.objects.filter(
                    qr_user=self.request.user,
                    category=self.kwargs['category'],
                    id=self.kwargs['pk'],
                    )
                except TypeError as ex:
                    return {'message':"error"}

            return qr
