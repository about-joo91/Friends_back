from functools import partial
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post as PostModel
# Create your views here.
class PostView(APIView):
    def post(self, request):
        author_id = request.user.id
        request.data['author_id'] = author_id
        post_serializer = PostSerializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({
            "message" : "게시글 업로드 되었습니다."
        }, status=status.HTTP_200_OK)
    def get(self, request):
        cur_user = request.user
        posts = PostModel.objects.filter(author = cur_user)
        return Response(
            PostSerializer(posts, many=True).data,
            status=status.HTTP_200_OK
        )
    def put(self, request,post_id):
        author_id = request.user.id
        request.data['author_id'] = author_id
        cur_post = PostModel.objects.get(id= post_id)
        post_serializer = PostSerializer(cur_post, data=request.data, partial=True)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({
            "message" : "게시글이 수정되었습니다."
        },status=status.HTTP_200_OK)
    def delete(self, request, post_id):
        target_post = PostModel.objects.get(id=post_id)
        target_post.delete()
        return Response({
            "message":"삭제가 완료 되었습니다."
        },status=status.HTTP_200_OK)