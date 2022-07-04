from django.contrib import admin

from .models import Post as PostModel
from .models import SavePost as SavePostModel
from .models import PostImg as PostImgModel

# Register your models here.

admin.site.register(PostModel)
admin.site.register(SavePostModel)
admin.site.register(PostImgModel)