from django.db import models

from joo_test.models import Post as PostModel

# Create your models here.
class Comment(models.Model):
    class Meta:
        db_table = "comments"
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)        
    post = models.ForeignKey('joo_test.Post', on_delete=models.CASCADE)
    comment = models.TextField("댓글", max_length=128)
    created_date = models.DateField("생성 날짜", auto_now_add=True)
