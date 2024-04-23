from rest_framework import serializers
from django.db import transaction
from . import models


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ['id', 'title']

class AddAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['name_account', 'game', 'decription', 'price', 'image'] 

class AccountSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    class Meta:
        model = models.Account
        fields = ['id', 'name_account', 'game', 'decription', 'price', 'image']  

class SimpleAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'name_account', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    account = SimpleAccountSerializer(read_only=True)
    class Meta:
        model = models.CartItem
        fields = ['id', 'cart', 'account']

class AddUpdateDeleteCartItemSerializer(serializers.ModelSerializer):
    def validate_cart_id(self, cart_id):
        if not models.Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given ID was found.')
        return cart_id
    def create(self, validated_data):
        # print(validated_data)
        try:
            cartitem = models.CartItem(**validated_data)
            cartitem.cart_id = self.context['cart_id']
            cartitem.save()
            return cartitem 
        except:
            raise serializers.ValidationError('this account sould out!')
    class Meta:
        
        model = models.CartItem
        fields = ['id', 'account']

class CartSerailizer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    def create(self, validated_data):
        # print(validated_data)
        if self.context['user_id']:
            if not models.Cart.objects.filter(user_id=self.context['user_id']).exists():
                cart = models.Cart(**validated_data)
                cart.user_id = self.context['user_id']
                cart.save()
                return cart
            
            else:
                raise serializers.ValidationError('cart with this user already exist!')
        else: raise serializers.ValidationError('authorization failed')
    class Meta:
        model = models.Cart
        fields = ['id', 'items','created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    account = SimpleAccountSerializer()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'account']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    def create(self, validated_data):
        with transaction.atomic():
            user_id = self.context['user_id']
            cart = models.Cart.objects.get(user_id=user_id)
            cart_items = models.CartItem.objects.filter(cart=cart)
            order = models.Order.objects.create(user_id=user_id)
            order_items = [
                models.OrderItem(
                    order=order,
                    account=item.account,
                ) for item in cart_items
            ]
            models.OrderItem.objects.bulk_create(order_items)

            models.Cart.objects.filter(pk=cart.id).delete()
            return order


    class Meta:
        model = models.Order
        fields = ['id', 'items','placed_at', 'payment_status']
        extra_kwargs = {
            "payment_status": {"read_only": True},
        }

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['payment_status']




