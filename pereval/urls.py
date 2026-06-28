from django.urls import path

from .views import SubmitDataAPIView, index

urlpatterns = [
    path('submitData/', SubmitDataAPIView.as_view()),
    path('submitData/<int:pk>/', SubmitDataAPIView.as_view()),
    path('', index),
]