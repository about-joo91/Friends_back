from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from joo_test.models import Post as PostModel
from .models import Like as LikeModel

#from .serializers import LikeSerializer


# Create your views here.
class LikeView(APIView): 
    def post(self, request, post_id):
        user = request.user
        post = PostModel.objects.get(id=post_id)
        new_like_obj, created = LikeModel.objects.get_or_create(like_user = user, like_post=post)
        if created:
            new_like_obj.save()
            return Response({"message": "좋아요 완료!"}, status=status.HTTP_200_OK)
        else:
            new_like_obj.delete()
            return Response({"message": "좋아요 취소!"}, status=status.HTTP_200_OK)        
