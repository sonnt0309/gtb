from django.shortcuts import render
from .models import PostalCode
from django.views.generic import View
from django.http import JsonResponse
from rest_framework import generics
from .serializers import PostTalCodeSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class PostalCodeList(View):
    def get(self, request, zipCode):
        result = list(PostalCode.objects.filter(zip=zipCode)[:1].values())
        data = dict()
        data['result'] = result
        return JsonResponse(data)


class PostalCodeViews(generics.ListAPIView):

    def get(self, request):
        try:
            postal_code = PostalCode.objects.all()
            paginator = Paginator(postal_code, 20)
            page = request.GET.get('page')
            try:
                postal_code = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                postal_code = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                postal_code = paginator.page(paginator.num_pages)
            serializer_class = PostTalCodeSerializer(postal_code, many=True)
        except (ValueError, KeyError) as e:
            return Response({
                'code': 400,
                'message': 'Delete error: %s' % str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('err in delete user:', error)
            return Response({
                'code': 500,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'code': 200,
            'data': serializer_class.data,
            'message': 'OKE'
        }, status=status.HTTP_200_OK)


class PostalCodeDetail(generics.RetrieveAPIView):

    def get(self, request, pk):
        try:
            postal_code = PostalCode.objects.get(id=pk)
            serializer_class = PostTalCodeSerializer(postal_code)
        except (ValueError, KeyError) as e:
            return Response({
                'code': 400,
                'message': 'Postal code error: %s' % str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except (ObjectDoesNotExist, ValueError) as error:
            return Response({
                'code': 404,
                'message': 'Postal code not found'
            }, status= status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print('err in delete user:', error)
            return Response({
                'code': 500,
                'message': 'Internal error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'code': 200,
            'data': serializer_class.data,
            'message': 'OKE'
        }, status=status.HTTP_200_OK)