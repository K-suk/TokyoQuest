from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import SocialLoginSerializer
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'contact_address')
        
class CustomSocialLoginSerializer(SocialLoginSerializer):
    def validate(self, attrs):
        # まずは通常のバリデーション処理を行う
        data = super().validate(attrs)
        # バリデーション後にエラーがあればログ出力する（ここではエラーが発生しなければ出力されない）
        if self.errors:
            logger.error("SocialLogin validation errors: %s", self.errors)
        return data