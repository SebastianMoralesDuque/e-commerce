from rest_framework import serializers
from .models import User, Category, Product, ShoppingCart, Order, ShippingAddress, PaymentMethod, Transaction, Review, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'address']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ShippingAddress
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    payment_method = PaymentMethodSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Image
        fields = '__all__'
