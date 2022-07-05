from django.urls import path
from . import views

urlpatterns = [
    path('mypage/<int:user_id>', views.MypageView.as_view()),
    path('likedpage/<int:user_id>', views.LikedPageView.as_view()),
    path('like/<int:post_id>', views.LikeView.as_view()),
    path('bookmark/', views.BookmarktView.as_view()),
    path('bookmark/<int:post_id>', views.BookmarktView.as_view()),
]