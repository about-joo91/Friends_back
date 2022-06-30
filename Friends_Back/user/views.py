from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from user.models import User as UserModel
from user.serializers import UserSerializer



class UserView(APIView):
    permission_classes = [permissions.AllowAny]

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
