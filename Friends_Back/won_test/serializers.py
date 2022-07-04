# from rest_framework import serializers
# from .models import Like as LikeModel


# class LikeSerializer(serializers.ModelSerializer):
#     like_post = serializers.SerializerMethodField()
#     def get_like_post(self, obj):
#         like_posts = obj.like_post.id
#         return like_posts
#     like_user = serializers.SerializerMethodField()
#     def get_like_user(self, obj):
#         like_users = obj.like_user.id
#         return like_users
    
#     class Meta:
#         model = LikeModel
#         fields = ["like_post", "like_user"]