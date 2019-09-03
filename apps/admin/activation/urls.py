from django.urls import path
from . import views

urlpatterns = [
    path('', views.activateLisence, name='activationRoot'),
    path('getUserByLicenseId/<str:license_id>', views.ActivationCustomView.as_view(), name='activation_custom_view'),
    path('getListActivationByLicenseOfUser/<int:user_id>', views.ListActivationByLicenseOfUser.as_view()),
    path('detail/<int:id>', views.DetailActivation.as_view()),
    path('update/<int:id>', views.UpdateActivation.as_view()),
]
