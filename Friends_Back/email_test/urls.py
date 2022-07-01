from django.urls import path

from . import views
urlpatterns = [
    path('',views.EmailSendView.as_view())
]
