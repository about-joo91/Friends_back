from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel
# Create your views here.
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        my_follows = UserModel.objects.filter(followee = request.user)
        return Response({"my_follows" : list(my_follows.values('id'))}, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        user = request.user
        clicked_user = UserModel.objects.get(id=user_id)

        if user.follow.filter(id = clicked_user.id):
            user.follow.remove(clicked_user)
            my_follows = UserModel.objects.filter(followee = user)
            return Response({"my_follows" : list(my_follows.values('id'))}, status=status.HTTP_200_OK)
        user.follow.add(clicked_user)
        my_follows = UserModel.objects.filter(followee = user)
        return Response({"my_follows" : list(my_follows.values('id'))}, status=status.HTTP_400_BAD_REQUEST)