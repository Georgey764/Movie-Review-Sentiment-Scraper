from rest_framework import serializers
from restAPI.models import Stocks

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ['id', 'symbol']