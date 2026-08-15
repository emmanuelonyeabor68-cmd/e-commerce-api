from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('cart.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
