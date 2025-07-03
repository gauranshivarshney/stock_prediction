from django.urls import path
from .views import PredictAPIView, UserPredictionsAPIView

urlpatterns = [
    path('predict/', PredictAPIView.as_view(), name='predict'),
    path('predictions/', UserPredictionsAPIView.as_view(), name='predictions'),
]
