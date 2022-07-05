from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models.query_utils import Q

from bookmark_test.serializers import BookmarkSerializer
from joo_test.models import SavePost as SavePostModel
from joo_test.models import Post as PostModel
from joo_test.models import PostImg as PostImgModel
from joo_test.serializers import PostSerializer
# Create your views here.


class BookmarktView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        bookmark = SavePostModel.objects.filter(save_user=request.user)
        posts = list(map(lambda x: x.save_post, bookmark))
        print(posts)
        return Response({"posts": PostSerializer(posts, many=True).data},
            status=status.HTTP_200_OK
        )        
    def post(self, request, post_id):
        print(post_id)
        save_user = request.user.id
        save_post = PostModel.objects.get(id=post_id)
        same_save = SavePostModel.objects.filter(Q(save_user=save_user) & Q(save_post=save_post))
        if not same_save:
            data = {
                "save_user": save_user,
                "save_post": save_post.id
            }
            bookmakrserializer = BookmarkSerializer(data=data)
            if bookmakrserializer.is_valid(raise_exception=True):
                bookmakrserializer.save()
                return Response({"messge":"저장이 완료되었습니다!"},status=status.HTTP_200_OK)
            return Response({"messge":"이미 저장된 게시글 입니다"},status=status.HTTP_400_BAD_REQUEST)
        return Response(bookmakrserializer.errors)
    def delete(self, request, post_id):
        save_user = request.user.id
        save_post = PostModel.objects.get(id=post_id)
        same_save = SavePostModel.objects.filter(Q(save_user=save_user) & Q(save_post=save_post))
        if same_save:
            same_save.delete()
            return Response ({"messge","삭제가 완료되었습니다!"},status=status.HTTP_200_OK)
        return Response({"messge","저장된 게시글이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)