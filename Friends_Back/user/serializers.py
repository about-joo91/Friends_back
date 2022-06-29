from user.models import User as UserModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):

        return data

    def create(self, validated_data):
        print("validated_data : ", validated_data)
        password = validated_data.pop("password")

        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user


    def update(self, instance, validated_data):


        return instance


    class Meta:
        model = UserModel
        fields = ["username", "password", "nickname"]

        extra_kwargs = {
            'password': {'write_only': True},
            'username': {
                'error_messages': {
                    'required': 'username을 입력해주세요.',
                    'invalid': '알맞은 형식의 username을 입력해주세요.'
                    },
                    'required': False
                    },
            }