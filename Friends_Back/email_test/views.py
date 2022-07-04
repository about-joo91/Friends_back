from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import Google

class GoogleAuth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cur_user = request.user.id
        cur_user_email = Google.create_service(cur_user)
        return Response({
            "cur_user_email" : cur_user_email
        },status=status.HTTP_200_OK)

class SendEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cur_user = request.user.id
        email_from = request.data['email_from']
        email_to = request.data['email_to']
        email_content = request.data['email_content']
        email_title = request.data['email_title']
        Google.gmail_send_message(
            email_to = email_to,
            email_from = email_from,
            email_title= email_title,
            email_content = email_content,
            user_id= cur_user)
        return Response({
            "message" : "이메일을 보냈습니다."
            }, status=status.HTTP_200_OK)