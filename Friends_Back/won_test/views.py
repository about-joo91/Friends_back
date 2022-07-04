from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from joo_test.models import Post as PostModel
from .models import Like as LikeModel

from user.serializers import UserSerializer
from .serializers import MypageSerializer

# Create your views here.
class LikeView(APIView): 
    def post(self, request, post_id):
        user = request.user
        post = PostModel.objects.get(id=post_id)
        new_like_obj, created = LikeModel.objects.get_or_create(user = user, post=post)
        if created:
            new_like_obj.save()
            return Response({"message": "좋아요 완료!"}, status=status.HTTP_200_OK)
        else:
            new_like_obj.delete()
            return Response({"message": "좋아요 취소!"}, status=status.HTTP_200_OK)        


class MypageView(APIView):
    def get(self, request, user_id):
        user = request.user
        posts = PostModel.objects.filter(author=user)
        post_serializer_data = MypageSerializer(posts, many=True).data
        user_serializer_data = UserSerializer(user).data
        return Response({"posts": post_serializer_data, "user":user_serializer_data}, status=status.HTTP_200_OK)
        
        
        