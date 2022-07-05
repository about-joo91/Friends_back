from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from joo_test.models import Post as PostModel
from .models import Like as LikeModel

from user.serializers import UserSerializer
from joo_test.serializers import PostSerializer



# Create your views here.
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id):
        user = request.user
        posts = PostModel.objects.filter(author=user)
        post_serializer_data = PostSerializer(posts, many=True).data
        user_serializer_data = UserSerializer(user).data
        return Response({"posts": post_serializer_data, "user":user_serializer_data}, status=status.HTTP_200_OK)
        
        
class LikedPageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id):
        user = request.user
        posts = LikeModel.objects.filter(user=user)
        post_ids = [obj.post_id for obj in posts]
        post_objects = [PostModel.objects.get(id=id) for id in post_ids]
        likepage_serializer_data = PostSerializer(post_objects, many=True).data
        user_serializer_data = UserSerializer(user).data
        return Response({"posts": likepage_serializer_data, "user": user_serializer_data}, status=status.HTTP_200_OK)
        
        
        