from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from . import models, serializers

class AccountViewSet(ModelViewSet):
    queryset = models.Account.objects.all()
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT","DELETE"]:
            return serializers.AddAccountSerializer
        else:
            return serializers.AccountSerializer

class GameViewSet(ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

class CartViewSet(ModelViewSet):
    def get_serializer_context(self):
         return {'user_id': self.request.user.id}
        
    # def get_permissions(self):
    #     return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Cart.objects.all()
        else: 
            return models.Cart.objects.filter(user_id=user.id)
    serializer_class = serializers.CartSerailizer

class CartItemViewSet(ModelViewSet):
    def get_serializer_context(self):
         return {'cart_id': self.kwargs['cart_pk']}
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return serializers.AddUpdateDeleteCartItemSerializer
        else:
            return serializers.CartItemSerializer
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).all()
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    # def get_permissions(self):
    #     if self.request.method in ['PATCH', 'DELETE']:
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.UpdateOrderSerializer
        else:
            return serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Order.objects.all()
        return models.Order.objects.filter(user_id=user.id) 