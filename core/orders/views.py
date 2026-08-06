from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart
from rest_framework import viewsets

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user.is_authenticated and request.user.is_staff

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'head', 'options'] #no full put or delete


    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        with transaction.atomic():
            items = (
                cart.items
                .select_related('product')
                .select_for_update(of=('product',))
            )

            if not items.exists():
                return Response({'error': 'Cart is empty'}, status=400)

            # validate stock BEFORE creating anything
            for item in items:
                items.products.refresh_from_db()
                if item.quantity > item.product.stock:
                    return Response(
                        {'error': f'Not enough stock for {item.product.name}'}, status=400
                    )

                total = sum(item.product.price * item.quantity for item in items)
                order = Order.objects.create(user=request.user, total=total)

                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        price=item.product.price,
                        quantity=item.quantity,
                    )
                    item.product.stock -= item.quantity
                    item.product.save()

                items.delete()  # clear cart

            return Response(OrderSerializer(order).data, status=201)
