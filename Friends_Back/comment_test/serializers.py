from rest_framework import serializers

from comment_test.models import Comment as CommentModel

class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print("validated_data : ", validated_data)
        user = validated_data.pop("user")
        comment = CommentModel(**validated_data)
        
        comment.user = user
        comment.save()
        
        return comment
    class Meta:
        model = CommentModel
        fields = ["user", "comment", "post"]
