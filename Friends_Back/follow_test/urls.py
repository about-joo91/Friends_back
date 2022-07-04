from django.urls import path

from follow_test import views
urlpatterns = [
    path('', views.FollowView.as_view()),
    path('<int:user_id>', views.FollowView.as_view()),
]