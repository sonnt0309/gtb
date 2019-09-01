from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.PostalCodeViews.as_view()),
    path('<int:pk>/', views.PostalCodeDetail.as_view()),
    path('list/<str:zipCode>', views.PostalCodeList.as_view(), name='postal_code_list'),
]