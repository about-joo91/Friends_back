from django.urls import path

from comment_test import views
urlpatterns = [
    path('<int:post_id>', views.CommentView.as_view()),
]