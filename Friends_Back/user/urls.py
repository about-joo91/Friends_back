from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from user import views
urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('sign_up/', views.UserView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
