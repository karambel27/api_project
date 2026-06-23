from django.urls import path

from .views import SubmitDataAPIView


urlpatterns = [
    path('submitData/', SubmitDataAPIView.as_view()),
    path('submitData/<int:pk>/', SubmitDataAPIView.as_view()),
]