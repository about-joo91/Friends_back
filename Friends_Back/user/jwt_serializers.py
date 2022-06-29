from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CoustomJWTSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['username'] = user.username
        token['fullname'] = user.fullname

        return token