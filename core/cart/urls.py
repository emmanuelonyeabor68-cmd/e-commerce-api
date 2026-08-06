from rest_framework.routers import DefaultRouter
from .views import CartView, CartItemViewSet

router = DefaultRouter()
router.register('cart', CartView, basename='cart')
router.register('cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = router.urls