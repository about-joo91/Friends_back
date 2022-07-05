from rest_framework import serializers

from user.models import User as UserModel


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        return instance


    class Meta:
        model = UserModel
        fields = ["id","username", "password", "nickname"]

        extra_kwargs = {
            'password': {'write_only': True},
            'username': {
                'error_messages': {
                    'required': 'username을 입력해주세요.',
                    'invalid': '알맞은 형식의 username을 입력해주세요.'
                    },
                    'required': False
                    },
            'nickname': {
                'error_messages': {
                    'required': 'nickname을 입력해주세요.',
                    'invalid': '알맞은 형식의 nickname을 입력해주세요.'
                    },
                    'required': False
                    },
            }