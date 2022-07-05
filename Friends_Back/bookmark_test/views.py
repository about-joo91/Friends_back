from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.query_utils import Q

from bookmark_test.serializers import BookmarkSerializer, PostSerializer
from joo_test.models import SavePost as SavePostModel
from joo_test.models import Post as PostModel
from joo_test.models import PostImg as PostImgModel
# Create your views here.


class BookmarktView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        bookmark = SavePostModel.objects.filter(save_user=request.user)
        return Response(
            BookmarkSerializer(bookmark, many=True).data,
            status=status.HTTP_200_OK
        )
        
    def post(self, request, post_id):
        save_user = request.user.id
        save_post = PostModel.objects.get(id=post_id)
        same_save = SavePostModel.objects.filter(Q(save_user=save_user) & Q(save_post=save_post)).exists()
        if not same_save:
            bookmakrserializer = BookmarkSerializer(data=request.data)
            if bookmakrserializer.is_valid(raise_exception=True):
                bookmakrserializer.save(save_user=request.user ,save_post=save_post)
                return Response({"messge":"북마크가 완료되었습니다!"},status=status.HTTP_200_OK)
            return Response({"messge":"데이터 검증에 실패"},status=status.HTTP_400_BAD_REQUEST)
        same_save.delete()
        return Response ({"messge","북마크 취소가 완료되었습니다!"},status=status.HTTP_200_OK)