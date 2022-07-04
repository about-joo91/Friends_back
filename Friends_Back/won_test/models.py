from django.db import models

# Create your models here.
class Like(models.Model):
    post = models.ForeignKey("joo_test.Post", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)