from dataclasses import field
from pdb import post_mortem
from rest_framework import serializers
from user.models import User as UserModel
from .models import Post as PostModel, PostImg as PostImgModel


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.IntegerField(write_only= True)
    postimg = serializers.CharField(write_only= True)
    def get_author(self, obj):
        return obj.author.username
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
        fields = ["author", "author_id", "title", "content", "postimg"]