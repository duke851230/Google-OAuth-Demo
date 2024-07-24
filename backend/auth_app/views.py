import requests

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.conf import settings


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(
        detail=False, 
        methods=['get'], 
        url_path='csrf_token'
    )
    def get_csrf_token(self, request: Request) -> Response:
        """ 
        什麼都沒有的 API, 主要是用來讓前端可以與 Django 溝通。
        這樣 Django 才有機會塞 CSRF Token 到 Set-Cookie 中。
        """
        return Response({"success": True})
    
    @action(
        detail=False, 
        methods=['post'], 
        url_path='oauth/login'
    )
    def oauth_login(self, request: Request) -> Response:
        """
        當前端進行完 Google 授權請求後，會執行這隻 API 來完成登入驗證。
        1. 透過授權請求返回的 code 與 redirect_uri 來獲取 access_token
        2. 透過 access_token 去獲取 Google 個人資訊
        3. 依照 Google 個人資訊的信箱來創建 User
        4. 生成 JWT 供之後的 API 認證用
        """
        code: str = request.data.get("code")
        redirect_uri: str = request.data.get("redirect_uri")
        access_token: str = self._get_google_access_token(code, redirect_uri)
        
        google_user_info: dict = self._get_google_user_info(access_token)
        email: str = google_user_info["email"]

        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)  # 生成 JWT

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    
    def _get_google_access_token(self, code: str, redirect_uri: str) -> str:
        """
        透過前端傳來的 code 與 redirect_uri 來獲取 access_token。
        """
        token_url: str = settings.GOOGLE_TOKEN_BASE_URL
        client_id: str = settings.GOOGLE_CLIENT_ID
        client_secret: str = settings.GOOGLE_CLIENT_SECRET
        
        response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        })
        
        result: dict = response.json()
        access_token: str = result.get('access_token')
        token_type: str = result.get('token_type')
        print(f"{token_type=} {access_token=}")

        return f'{token_type} {access_token}'
    
    def _get_google_user_info(self, access_token: str) -> dict:
        """
        透過 access_token 去獲取 Google 個人資訊。
        """
        user_info_url: str = settings.GOOGLE_USER_INFO_BASE_URL

        response = requests.get(
            user_info_url, 
            headers={
                'Authorization': access_token
            }
        )
        user_info = response.json()
        print(f"{user_info=}")
        
        return user_info


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(
        detail=False, 
        methods=['get'], 
        url_path='info'
    )
    def info(self, request: Request) -> Response:
        # JWTAuthentication 類會幫我們處理下列資訊
        print(f"{request.auth=}")  # {'token_type': 'access', 'exp': 1721818695, 'iat': 1721818395, 'jti': '894dd1cf61104da38d47c091836d6019', 'user_id': 1}
        print(f"{request.user=}")  # <User: duke.chen@tagtoo.com>

        data: dict = model_to_dict(request.user)
        return Response(data)

