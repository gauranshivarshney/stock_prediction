from rest_framework import serializers

class StockDataSerializer(serializers.Serializer):
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()  