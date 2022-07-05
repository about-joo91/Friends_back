from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, nickname, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            nickname=nickname
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, nickname, password=None):
        user = self.create_user(
            username = username,
            password = password,
            nickname = nickname
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    follow = models.ManyToManyField("User", related_name="followee") # 이부분만 기존의 모델에서 추가를 했습니다.

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
        
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
