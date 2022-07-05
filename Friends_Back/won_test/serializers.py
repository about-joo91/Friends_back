from rest_framework import serializers
from joo_test.serializers import PostSerializer
from joo_test.models import Post as PostModel
from .models import Like as LikeModel



class LikeSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    def get_nickname(self, obj):
        return obj.user.username
    class Meta:
        model = LikeModel
        fields = ["nickname"]


class MypageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    img_url = serializers.SerializerMethodField(read_only=True)
    def get_author(self, obj):
        return obj.author.username
    def get_img_url(self, obj):
        return obj.postimg.img_url
    
    class Meta:
        model = PostModel
        fields = ["id", "title", "content", "author", "img_url"]
        
        

# class LikedPageSerializer(serializers.ModelSerializer):
#     posts = serializers.