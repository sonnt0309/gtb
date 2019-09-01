from django.urls import path
from . import views

urlpatterns = [
    path('getRelateInfoByActivateKey/<str:activate_key>', views.ExecutionStatusCustomView.as_view(), name='execution_status_custom_view'),
]