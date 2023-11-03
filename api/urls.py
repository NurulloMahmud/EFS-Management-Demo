from django.urls import path
from .views import GenerateEFScodeAPIView

urlpatterns = [
    path('generate-efs/', GenerateEFScodeAPIView.as_view(), name='generate-efs'),
]