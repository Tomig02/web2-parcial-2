from rest_framework import serializers
from .models import UserMessages
import requests

class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = '__all__'

class ProductoSerializer(serializers.Serializer):
    url = serializers.CharField(allow_blank=True)
    title = serializers.CharField()
    subtitle = serializers.CharField()
    text = serializers.CharField()
    price = serializers.CharField()
    price_usd = serializers.SerializerMethodField()

    def get_price_usd(self, obj):
        try:
            precio_pesos = float(obj['price'].replace('.', ''))
        except (ValueError, KeyError):
            return "N/A"
        try:
            response = requests.get('https://dolarapi.com/v1/dolares/oficial', timeout=3)
            if response.status_code == 200:
                valor_dolar = response.json().get('venta', 1000)

                precio_convertido = precio_pesos / valor_dolar
                return f"{precio_convertido:.2f}"
        except Exception:
            pass
            
        return "N/A"