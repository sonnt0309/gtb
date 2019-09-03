from django.urls import path
from . import views

urlpatterns = [
    path('updateStatusApp', views.updateStatusApp, name='updateStatusApp'),
    path('getStatusApp', views.getStatusApp, name='getStatusApp'),
    path('release', views.releaseStatusApp, name='releaseStatusApp'),
    path('getRelateInfoByActivateKey/<str:activate_key>', views.ExecutionStatusCustomView.as_view(), name='execution_status_custom_view'),
]