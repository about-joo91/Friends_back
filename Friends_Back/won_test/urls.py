from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:post_id>', views.LikeView.as_view()),
]