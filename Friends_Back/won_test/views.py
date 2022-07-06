from django.shortcuts import render
from django.db.models.query_utils import Q
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Like as LikeModel
from joo_test.models import Post as PostModel
from joo_test.models import PostImg as PostImgModel
from joo_test.models import SavePost as SavePostModel

from user.serializers import UserSerializer
from joo_test.serializers import PostSerializer
from .serializers import BookmarkSerializer



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
        new_like_obj.delete()
        return Response({"message": "좋아요 취소!"}, status=status.HTTP_200_OK)        


class MypageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user
        posts = PostModel.objects.filter(author=user)
        post_serializer_data = PostSerializer(posts, many=True, context={'request':request}).data
        user_serializer_data = UserSerializer(user).data
        return Response({"posts": post_serializer_data, "user":user_serializer_data}, status=status.HTTP_200_OK)
        
        
class LikedPageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user
        post_ids = list(map(lambda x: x.post_id, LikeModel.objects.filter(user=user)))
        print(LikeModel.objects.filter(user=user))
        liked_posts = PostModel.objects.filter(id__in = post_ids)
        likedpage_serializer_data = PostSerializer(liked_posts, many=True, context={'request':request}).data
        user_serializer_data = UserSerializer(user).data
        return Response({"posts": likedpage_serializer_data, "user": user_serializer_data}, status=status.HTTP_200_OK)
        
        

class BookmarktView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        bookmark = SavePostModel.objects.filter(save_user=request.user)
        posts = list(map(lambda x: x.save_post, bookmark))
        print(posts)
        return Response({"posts": PostSerializer(posts, many=True, context={'request':request}).data},
            status=status.HTTP_200_OK
        )        
    def post(self, request, post_id):
        save_user = request.user.id
        save_post = PostModel.objects.get(id=post_id)
        same_save = SavePostModel.objects.filter(Q(save_user=save_user) & Q(save_post=save_post))
        if not same_save.exists():
            bookmakrserializer = BookmarkSerializer(data=request.data)
            if bookmakrserializer.is_valid(raise_exception=True):
                bookmakrserializer.save(save_user=request.user ,save_post=save_post)
                return Response({"messge":"북마크가 완료되었습니다!"},status=status.HTTP_200_OK)
            return Response({"messge":"데이터 검증에 실패"},status=status.HTTP_400_BAD_REQUEST)
        same_save.delete()
        return Response ({"messge","북마크 취소가 완료되었습니다!"},status=status.HTTP_200_OK)
    
    def delete(self, request, post_id):
        save_user = request.user.id
        save_post = PostModel.objects.get(id=post_id)
        same_save = SavePostModel.objects.filter(Q(save_user=save_user) & Q(save_post=save_post))
        if same_save:
            same_save.delete()
            return Response ({"messge","삭제가 완료되었습니다!"},status=status.HTTP_200_OK)
        return Response({"messge","저장된 게시글이 없습니다!"},status=status.HTTP_400_BAD_REQUEST)