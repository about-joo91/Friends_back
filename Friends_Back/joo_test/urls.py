from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # 기본 JWT access(인증토큰) 토큰 발급 view
    TokenRefreshView, # JWT Refresh 토큰 발급 view (새로고침같은) 
    #인증 토큰을 계속 재발급 받기위한
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.PostView.as_view()),
    path('<int:post_id>', views.PostView.as_view()),
    path('priview/',views.PreviewView.as_view()),
    
]