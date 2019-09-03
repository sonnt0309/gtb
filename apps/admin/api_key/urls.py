from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.GenerateKey.as_view()),
    path('linkDown/', views.LinkDown.as_view()),
    path('showKey/', views.ShowKey.as_view()),
]