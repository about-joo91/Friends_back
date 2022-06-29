from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
    path('api/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sparta/token/', views.CustomTokenObtainPairview.as_view()),
    path('api/authonly/', views.OnlyAuthenticatedUserView.as_view()),
]
