from django.shortcuts import render
import jwt

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CommentSerializer
from .models import Comment as CommentModel
# Create your views here.

class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
	
    authentication_classes = [JWTAuthentication]
    def get(self, request, post_id):
        post_comment = CommentModel.objects.filter(post = post_id)
        return Response(CommentSerializer(post_comment, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request, post_id):
        user = request.user
        request.data['user'] = user.id
        request.data['post'] = post_id
        print(request.data)
        comment_serializer = CommentSerializer(data=request.data, context={"request":request})
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)