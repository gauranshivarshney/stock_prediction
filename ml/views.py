from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockDataSerializer
from .prediction import predict_stock
from ml.utils import predict_next_price
from frontend.models import Prediction
from django.utils.timezone import localtime

class PredictAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ticker = request.data.get("ticker", "").strip()
        if not ticker:
            return Response({"error": "Ticker is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = predict_next_price(ticker.upper())
            Prediction.objects.create(
                user=request.user,
                ticker=ticker.upper(),
                predicted_price=result['next_day_price'],
                rmse=result['rmse'],
                r2=result['r2']
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserPredictionsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
        data = [
            {
                "ticker": p.ticker,
                "predicted_price": p.predicted_price,
                "rmse": p.rmse,
                "r2": p.r2,
                "created_at": localtime(p.created_at).strftime('%Y-%m-%d %H:%M')
            }
            for p in predictions
        ]
        return Response(data, status=status.HTTP_200_OK)