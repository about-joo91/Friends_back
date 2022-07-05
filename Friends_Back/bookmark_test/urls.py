from django.urls import path
from bookmark_test import views
urlpatterns = [
    path('', views.BookmarktView.as_view()),
    path('<int:post_id>', views.BookmarktView.as_view()),
]