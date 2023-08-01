from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializer
from bs4 import BeautifulSoup
import requests
from decimal import Decimal


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'


class ScrapeSiteSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        products = []
        try:
            response = requests.get(validated_data['url'])
        except:
            raise serializers.ValidationError({
                'error': 'Server Error'
            })
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            products_div = soup.find_all('div', {'class': 'itm col'})
            for product in products_div:
                try:
                    desc = {
                        'image': product.find('img').get('data-src'),
                        'name': product.find('div', {'class': 'name'}).text.strip(),
                        'price': Decimal(product.find('div', {'class': 'prc'}).text.strip().replace(',', '').split(' ')[-1])
                    }
                    products.append(desc)
                except:
                    pass
            bulk_products = [Product(name=product['name'],
                                     price=product['price'],
                                     image=product['image'],
                                     user=self.context['request'].user)
                             for product in products]
            products = Product.objects.bulk_create(bulk_products)
            return products
        else:
            raise serializers.ValidationError({
                'url': 'An error occurred'
            })

    def to_representation(self, instance):
        return {
            'products': ProductSerializer(instance, many=True).data
        }

