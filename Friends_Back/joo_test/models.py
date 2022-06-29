from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class PostImg(models.Model):
    post = models.OneToOneField('Post', on_delete=models.SET_NULL, null=True)
    img_url = models.URLField()

class SavePost(models.Model):
    save_user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    save_post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)