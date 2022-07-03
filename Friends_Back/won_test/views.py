from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from joo_test.models import Post as PostModel
from .models import Like as LikeModel

from .serializers import LikeSerializer


# Create your views here.
class LikeView(APIView):
    def get(self, request, post_id):
        user = request.user
        post = PostModel.objects.get(id=post_id)
        likes = LikeModel.objects.filter(like_post = post).order_by('-id')
        like_counts = len(likes)
        like_serializer = LikeSerializer(likes, many=True).data
        try:
            LikeModel.objects.get(like_user = user, like_post=post)
            liked = True
        except LikeModel.DoesNotExist:
            liked = False
        return Response({"like_model": like_serializer, "like_counts": like_counts, "liked": liked}, status=status.HTTP_200_OK)
        
    
    def post(self, request, post_id):
        user = request.user
        post = PostModel.objects.get(id=post_id)
        new_like_obj, created = LikeModel.objects.get_or_create(like_user = user, like_post=post)
        if created:
            new_like_obj.save()
            return Response({"message": "좋아요 완료!"}, status=status.HTTP_200_OK)
        return Response({"message": "이미 좋아요 완료"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, post_id):
        user = request.user
        try:
            liked_post = LikeModel.objects.get(like_user=user, like_post=post_id)
            liked_post.delete()
            return Response({"message": "좋아요 취소!"}, status=status.HTTP_200_OK)
        except LikeModel.DoesNotExist:
            return Response({'message': '존재하지 않는 오브젝트입니다!'}, status=status.HTTP_400_BAD_REQUEST)