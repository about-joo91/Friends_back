from rest_framework import serializers

from django.db.models.query_utils import Q


from joo_test.models import SavePost as Save_postModel
from user.models import User as UserModel
from joo_test.models import Post as PostModel
from joo_test.models import PostImg as PostImgModel
from joo_test.serializers import PostSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save_postModel
        fields = ["save_user","save_post"]

class PostSerializer(serializers.ModelSerializer):
    bookmark = serializers.SerializerMethodField()
    def get_bookmark(self,obj):
        return obj.title, obj.postimg.img_url
    class Meta:
        model = PostModel
        fields =["bookmark"]