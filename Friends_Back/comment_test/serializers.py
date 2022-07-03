from rest_framework import serializers

from comment_test.models import Comment as CommentModel
from user.models import User as UserModel

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    def get_author(self,obj):
        
        return obj.user.nickname

    def create(self, validated_data):
        user = validated_data.pop("user")
        comment = CommentModel(**validated_data)

        comment.user = user
        comment.save()
        return comment
    
    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
    class Meta:
        model = CommentModel
        fields = ["id", "author",'created_date', 'user', "comment", "post"]

        extra_kwargs = {
            'post': {'write_only': True}, # default : False
            }
