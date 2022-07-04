from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import Google

class GoogleAuth(APIView):
    def get(self, request):
        cur_user_email = Google.create_service()
        return Response({
            "cur_user_email" : cur_user_email
        },status=status.HTTP_200_OK)

class SendEmail(APIView):
    def post(self,request):
        email_from = request.data['email_from']
        email_to = request.data['email_to']
        email_content = request.data['email_content']
        email_title = request.data['email_title']
        Google.gmail_send_message(
            email_to = email_to,
            email_from = email_from,
            email_title= email_title,
            email_content = email_content)
        return Response({
            "message" : "이메일을 보냈습니다."
            }, status=status.HTTP_200_OK)