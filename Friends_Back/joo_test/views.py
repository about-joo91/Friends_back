import datetime
import os 
from urllib import parse

import boto3
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import PostSerializer
from .models import Post as PostModel
from user.serializers import UserSerializer
from user.models import User as UserModel
from config import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY
# Create your views here.


class PreviewView(APIView):
    def post(self,request):
        
        choice_char = request.data['choice']

        s3= boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        input_file = request.FILES['postimg']
        input_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        s3.put_object(
                ACL= "public-read",
                Bucket = "bucketfriends",
                Body =input_file,
                Key = input_name,
                ContentType = input_file.content_type,
            )
        #### 테스트 코드 입니다. #####

        # input_file = request.FILES['postimg']
        # input_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        # event_name = str(request.user.id) + "preview"
        # event_file = request.FILES['eventimg']
        # file_list = []
        # file_list.append(input_file)
        # file_list.append(event_file)
        # name_list= []
        # name_list.append(input_name)
        # name_list.append(event_name)
        # for i in range(2):
        #     file = file_list[i]
        #     name = name_list[i]
        #     print(file,name)
        #     s3.put_object(
        #         ACL= "public-read",
        #         Bucket = "bucketfriends",
        #         Body =file,
        #         Key = name,
        #         ContentType = file.content_type,
        #     )
        #### 딥러닝 출력이랑 로직 합쳐야 작동 합니다 ######
        #### 합친 후 리턴 값 바꿔줘야 합니다 ####
        return Response(input_name,status=status.HTTP_200_OK)



class PostView(APIView):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            title = request.POST.get('title')
            content = request.POST.get('content')
            postimg = request.POST.get('postimg')
            author_id = request.user.id
            base_url = "https://bucketfriends.s3.ap-northeast-2.amazonaws.com/" + postimg
            post_datas = {
                "author_id": author_id,
                "title": title,
                "content": content,
                "postimg" : base_url,
            }
            post_serializer = PostSerializer(data=post_datas)
            post_serializer.is_valid(raise_exception=True)
            post_serializer.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        page_num = int(self.request.query_params.get('page_num'))

        cur_user = request.user
        post_models = PostModel.objects.filter(author = cur_user)
        
        my_followers = cur_user.follow.all()
        post_models |= PostModel.objects.filter(author__in = my_followers)
        post_models.order_by('-created_date')

        len_of_posts = len(post_models)
        posts = post_models[page_num *4 : (page_num+1) *4]

        my_post = PostModel.objects.filter(author = cur_user).order_by('-created_date').first()

        recommend_followers = UserModel.objects.none()
        for user_obj in my_followers:
            recommend_followers|= user_obj.follow.all()
        recommend_followers.exclude(id__in = my_followers).exclude(id=cur_user.id).order_by('-created_date')[:10]
        if len(recommend_followers) == 0:
            recommend_followers = UserModel.objects.all().exclude(
                    id__in = my_followers).exclude(id=cur_user.id).order_by('-created_date')[:10]

        return Response(
            {
                "cur_user" : UserSerializer(cur_user).data,
                "posts": PostSerializer(posts, many=True, context={'request' : request}).data,
                "my_post" : PostSerializer(my_post,context={'request': request}).data,
                "len_of_posts" : len_of_posts,
                "recommend_followers": UserSerializer(recommend_followers, many=True).data
            },
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