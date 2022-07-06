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

import warnings
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
import os
import skvideo.io
from skimage import img_as_ubyte
from first_order_model.demo import load_checkpoints, make_animation

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Create your views here.
import requests
import urllib.request 
from django.core.files.storage import default_storage 
 

class PreviewView(APIView):
    def post(self,request):
        
        # choice_char = request.data['choice']

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
                 Key = input_name + "origin.gif",
                 ContentType = input_file.content_type,
             )
        #### 테스트 코드 입니다. #####
        url = "https://bucketfriends.s3.ap-northeast-2.amazonaws.com/" + input_name + "origin.gif"
        with urllib.request.urlopen(url) as fh:
            with open(f'./input/{input_name}origin.gif', 'wb') as out: 
                out.write(fh.read())

        #input_file = request.FILES['postimg']
        #file_type = input_file.name.split(".")[-1]
      
        #input_name = date + "origin." + file_type
        
        #with open('/input/'+input_name+".gif", 'wb') as f:
        #    f.write(requests.get(url).content)

        #input_folder = "./input"
        #imageio.imwrite(os.path.join(input_folder, input_name), im, file_type )
        #imageio.mimsave(os.path.join(input_folder, input_name),input_file, format="GIF", duration=0.04)
        
                   
       # file_obj = request.data['file'] 
       # with default_storage.open('input/'+input_file.name, 'wb+') as destination:
        #    for chunk in file_obj.chunks():
         #       destination.write(chunk)
        # 딥러닝에 넣기
        warnings.filterwarnings("ignore")


       # open(input_file, "w").write(os.path.join(input_folder, input_name))
       # path = default_storage.save('tmp/somename.mp3', ContentFile(data.read()))
       
       # )
 
        
        #file = request.FILES['postimg'] 
        #input_name), ContentFile(file.read()))

        #입력사진
        source_image = imageio.imread(f'/home/ubuntu/Friends_Back/Friends_back/Friends_Back/friends_img/{choice_char}.jpeg')
        #source_image = imageio.imread(f'/home/ubuntu/Friends_Back/Friends_back/Friends_Back/friends_img/4.jpg')

        #입력영상
        driving_video = skvideo.io.vread(f"./input/{input_name}origin.gif")
       # driving_video  =  skvideo.io.vread(input_file.name)

        #Resize image and video to 256x256
        source_image = resize(source_image, (256, 256))[..., :3]
        driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
        
        # from demo import load_checkpoints
        target_folder = "/home/ubuntu/Friends_Back/Friends_back/Friends_Back/first_order_model/"
        generator, kp_detector = load_checkpoints(config_path=os.path.join(target_folder,'vox-256.yaml'),
                                    checkpoint_path=os.path.join(target_folder,'vox-cpk.pth.tar'))
        
        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
        
        result_folder = '/home/ubuntu/Friends_Back/Friends_back/Friends_Back/result'
        event_name = input_name + "deep.gif"
        
        #save resulting video
        imageio.mimsave(os.path.join(result_folder, event_name), [img_as_ubyte(frame) for frame in predictions], format="GIF")
        
        data = open(os.path.join(result_folder, event_name), 'rb')
        print(os.path.join(result_folder, event_name))
        #output_file = skvideo.io.vread(f"./result/{event_name}")
        #output_img = imageio.imread(f"./result/{event_name}")
       
        #s3_resource

       # s3.Bucket("bucketfriends").put_object(Body=data, Key=event_name, ACL= "public-read")




        s3.put_object(
             ACL= "public-read",
             Bucket = "bucketfriends",
             Body =data,
             Key = event_name,
             ContentType =input_file.content_type,
            )


        #from io import BytesIO 
       # from PIL import Image 
       # im = Image.new("RGB", (50, 50)) 
        #data = BytesIO() 
        #im.save(data, "gif") data.seek(0) # e.g. save to file import shutil 
       # with open("image.gif", "wb") as f: 
         #   shutil.copyfileobj(data, f)


        #s3 = boto3.client('s3') 
        #with open("FILE_NAME", "rb") as f: 
        #    s3.upload_fileobj(f, "BUCKET_NAME", "OBJECT_NAME")
        #### 딥러닝 출력이랑 로직 합쳐야 작동 합니다 ######
        #### 합친 후 리턴 값 바꿔줘야 합니다 ####)
        return Response(event_name,status=status.HTTP_200_OK)



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
                    id__in = my_followers).exclude(id=cur_user.id).order_by(
                '-created_date')[:10]

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
