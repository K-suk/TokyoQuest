from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import logging
from .serializers import UserSerializer, UserUpdateSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        logger.debug(f"Received refresh token: {refresh_token}")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except TokenError as e:
        if str(e) == 'Token is blacklisted':
            # トークンがすでにブラックリストに登録されている場合も正常終了として扱う
            return Response(status=status.HTTP_205_RESET_CONTENT)
        logger.error(f"Logout error: {str(e)}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not user.check_password(current_password):
        return Response({"detail": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        
        try:
            user_pk_bytes = force_bytes(user.pk)
            logger.debug(f"User PK as bytes: {user_pk_bytes}")  # ユーザーのプライマリーキーをバイト形式でログに出力
            uid = urlsafe_base64_encode(user_pk_bytes)
            logger.debug(f"Encoded UID: {uid}")
        except Exception as e:
            logger.error(f"Error encoding UID: {e}")
            return Response({"detail": "Error encoding UID"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        reset_link = f"http://localhost:3000/reset-password?uid={uid}&token={token}"
        logger.debug(f"Password reset link: {reset_link}")
        logger.debug(f"Generated token: {token}")
        
        subject = "Password Reset Requested"
        message = render_to_string('accounts/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        send_mail(subject, message, None, [user.email])
        
        return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    logger.debug(f"Request data: {request.data}")  # 受け取ったリクエストデータをログに出力

    if token is None:
        logger.error("Token is None")  # トークンがNoneの場合にログに出力
        return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # force_str を使用
        logger.debug(f"Decoded UID: {uid}")  # UIDをログに出力
        logger.debug(f"Received token: {token}")  # 受け取ったトークンをログに出力
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been reset"}, status=status.HTTP_200_OK)
        else:
            logger.debug("Invalid token")  # トークンが無効な場合にログに出力
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logger.error("Invalid request")  # 無効なリクエストの場合にログに出力
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)