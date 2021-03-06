from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel
from user.serializers import UserSerializer

class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    # permission_classes = [RegistedMoreThanAWeekUser]

    def get(self,request):
        all_users = UserModel.objects.all()
        return Response(UserSerializer(all_users, many=True).data, status= status.HTTP_200_OK)
        

    def post(self,request):

        user_serializer = UserSerializer(data=request.data, context={"request":request})
    
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        user = UserModel.objects.get(id=obj_id)
        user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request":request})

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        return Response({"message" : "delete method!!"})

# Create your views here.
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        user = request.user
        clicked_user = UserModel.objects.get(id=user_id)
        if user.follow.filter(id = clicked_user.id):
            user.follow.remove(clicked_user)
            return Response({
                "message" : "팔로우 취소"
            }, status=status.HTTP_200_OK)
        user.follow.add(clicked_user)
        return Response({
            "message" : "팔로우 성공"
        }, status=status.HTTP_200_OK)