from django.urls import path

from comment_test import views
urlpatterns = [
    path('', views.CommentView.as_view()),
    path('<int:obj_id>', views.CommentView.as_view()),
]