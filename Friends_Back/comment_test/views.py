from django.shortcuts import render

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
    def get(self, request, obj_id):
        # obj_id = post_id 입니다!
        post_comment = CommentModel.objects.filter(post = obj_id)
        return Response(CommentSerializer(post_comment, many=True).data, status=status.HTTP_200_OK)
       
    def post(self, request, obj_id):
        # obj_id = post_id 입니다!
        user = request.user
        request.data['user'] = user.id
        request.data['post'] = obj_id
        comment_serializer = CommentSerializer(data=request.data, context={"request":request})
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        # obj_id = comment_id 입니다!
        comment = CommentModel.objects.get(id=obj_id)
        comment_serializer = CommentSerializer(comment, data=request.data, partial=True)
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, obj_id):
        # obj_id = comment_id 입니다!
        comment = CommentModel.objects.get(id = obj_id)
        if comment:
            comment.delete()
            return Response({"message": "댓글삭제"}, status=status.HTTP_200_OK)
        return Response({"message": "댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)