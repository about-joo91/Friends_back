from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db.models import F, Q
from django.contrib.auth import authenticate, login, logout

from user.models import User as UserModel
from user.serializers import UserSerializer

from user.jwt_serializers import CoustomJWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

# 유저 조회, 회원가입, 수정, 삭제
class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    # permission_classes = [RegistedMoreThanAWeekUser]

    def get(self,request):
        all_users = UserModel.objects.all()
        return Response(UserSerializer(all_users, many=True).data, status= status.HTTP_200_OK)
        

    def post(self,request):
        print("request : ", request.data)
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

# 로그인, 로그아웃
class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password = password)
        if user:
            login(request,user)
            return Response({"message" : "login success!!"})
        return Response({"message" : "존재하지 않거나 틀린 계정입니다!!"})

    def delete(self, request):
        logout(request)
        return Response({"message" : "logout success!!"})


class CustomTokenObtainPairview(TokenObtainPairView):
    serializer_class = CoustomJWTSerializer

class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})