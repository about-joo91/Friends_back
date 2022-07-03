from django.db import models
from joo_test.models import Post as PostModel

# Create your models here.
class Like(models.Model):
    like_post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    like_user = models.ForeignKey("user.User", on_delete=models.CASCADE)