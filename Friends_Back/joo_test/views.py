from functools import partial
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post as PostModel
from config import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
from django.core import serializers
import boto3
from urllib import parse
import datetime
from django.http import HttpResponse
# Create your views here.


class PostView(APIView):
    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        try:
            s3= boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
            file = request.FILES['postimg']
            date = (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            s3.put_object(
                    ACL= "public-read",
                    Bucket = "bucketfriends",
                    Body =file,
                    Key = date,
                    # ContentType = file.content_type,
                    ContentType = file.content_type,
                )
            author_id = request.user.id
            base_url = "https://bucketfriends.s3.ap-northeast-2.amazonaws.com"
            image_url = parse.urljoin(base=base_url,url=str(date),allow_fragments=True)
            post_datas = {
                "author_id": author_id,
                "title": title,
                "content": content,
                "postimg" : image_url,
            }
            post_serializer = PostSerializer(data=post_datas)
            post_serializer.is_valid(raise_exception=True)
            post_serializer.save()

            
        
            return Response(date,status=status.HTTP_200_OK)

        except:
            return Response({"message" : "게시글 업로드 실패."}, status=status.HTTP_400_BAD_REQUEST)

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