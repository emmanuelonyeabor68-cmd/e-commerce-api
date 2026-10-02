from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'full_name', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'email', 'is_staff', 'date_joined')