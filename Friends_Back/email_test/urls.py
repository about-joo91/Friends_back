from django.urls import path

from . import views

urlpatterns = [
    path('',views.GoogleAuth.as_view()),
    path('send/', views.SendEmail.as_view()),
]
