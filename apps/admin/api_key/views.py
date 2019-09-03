from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from helper import hashers
from rest_framework import status
from django.http import FileResponse


# Create your views here.
class GenerateKey(generics.ListAPIView):

    def post(self, request, *args, **kwargs):
        try:
            password1 = request.data['password1']
            password2 = request.data['password2']

            if not password1 == password2:
                return Response({
                    'status': False,
                    'message': 'Password incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            hashers.generating_key(password1)
            publicKey = open("file_down/public_key.pem", "rb")
            publicKey = publicKey.read()
            privateKey = open("file_down/private_key.pem", "rb")
            privateKey = privateKey.read()

        except KeyError as error:
            print('generate key KeyError:', error)
            return Response({
                'status': False,
                'message': 'KeyError'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print('generate key error:', error)
            return Response({
                'status': False,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": True,
            "data": {
                'private_key': privateKey,
                'public_key': publicKey,
            },
            "message": 'Generate Key success!'
        }, status=status.HTTP_200_OK)


class LinkDown(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        response = FileResponse(open("file_down/public_key.pem", 'rb'), as_attachment=True)
        return response


class ShowKey(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            publicKey = open("file_down/public_key.pem", "rb")
            publicKey = publicKey.read()
            privateKey = open("file_down/private_key.pem", "rb")
            privateKey = privateKey.read()

        except Exception as error:
            print('err in add activation:', error)
            return Response({
                'status': False,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': True,
            "data": {
                'private_key': privateKey,
                'public_key': publicKey,
            },
            'message': 'Show key success!'
        }, status=status.HTTP_200_OK)
