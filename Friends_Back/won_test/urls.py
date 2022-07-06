from django.urls import path
from . import views

urlpatterns = [
    path('mypage', views.MypageView.as_view()),
    path('likedpage', views.LikedPageView.as_view()),
    path('like/<int:post_id>', views.LikeView.as_view()),
    path('bookmark/', views.BookmarktView.as_view()),
    path('bookmark/<int:post_id>', views.BookmarktView.as_view()),
]