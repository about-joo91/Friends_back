from rest_framework import serializers

from django.db.models.query_utils import Q


from joo_test.models import SavePost as Save_postModel
from user.models import User as UserModel
from joo_test.models import Post as PostModel
from joo_test.models import PostImg as PostImgModel
from joo_test.serializers import PostSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    save_post = serializers.SerializerMethodField()

    def get_save_post(self,obj):
        return PostSerializer(obj.save_post).data

    class Meta:
        model = Save_postModel
        fields = ["save_user","save_post"]

    extra_kwargs = {
            'save_user': {'write_only': True},
            }
