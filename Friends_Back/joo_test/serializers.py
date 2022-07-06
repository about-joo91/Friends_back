from rest_framework import serializers

from user.models import User as UserModel
from .models import Post as PostModel, PostImg as PostImgModel, SavePost as SavePostModel
from user.serializers import UserSerializer
from won_test.models import Like as LikeModel


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.IntegerField()
    postimg = serializers.CharField(write_only= True)
    img_url = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    bookmarked = serializers.SerializerMethodField(read_only=True)

    def get_bookmarked(self, obj):
        cur_user = self.context['request'].user
        return SavePostModel.objects.filter(save_post =obj, save_user = cur_user)
    def get_liked(self, obj):
        cur_user = self.context['request'].user
        return LikeModel.objects.filter(user = cur_user, post=obj).exists()

    def get_img_url(self, obj):
        return obj.postimg.img_url

    def get_author(self, obj):
        return UserSerializer(obj.author).data

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        author = UserModel.objects.get(id = author_id)
        post_img = validated_data.pop('postimg')
        new_post= PostModel.objects.create(
            author = author,
            **validated_data
        )
        new_post.save()
        PostImgModel(post= new_post, img_url =post_img).save()
        return new_post

    def update(self, instance, validated_data):
        post_img = validated_data.pop('postimg')
        for key, value in validated_data.items():
            setattr(instance,key,value)
        instance.save()
        new_post_img = PostImgModel.objects.get(post = instance)
        new_post_img.img_url = post_img
        new_post_img.save()
        return instance
        
    class Meta:
        model = PostModel
        fields = ["id","author","liked","bookmarked", "author_id", "title", "content", "postimg" ,"img_url"]
        extra_kwargs = {
            "id" : {"read_only" : True}
        }