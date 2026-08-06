from django.urls import path
from .views import CustomLoginView, CustomRefreshView, CustomLogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view()),
    path('refresh/', CustomRefreshView.as_view()),
    path('logout/', CustomLogoutView.as_view()),
]