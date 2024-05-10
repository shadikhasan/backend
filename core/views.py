from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from . import serializers
from . import renderers
from django.shortcuts import render

# M A N U A L L Y   G E N E R A T E   T O K E N
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, format=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {
                    'token':token,
                    'msg':'Registration Successful !'
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  



class UserLogInView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, format=None):
        serializer = serializers.UseLogInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.role == 4:
                    return Response(
                        {'error': 'You are not authorized to log in.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                token = get_tokens_for_user(user)
                return Response(
                    {
                        'token': token,
                        'msg':'LogIn Successful !'
                    }, 
                    status=status.HTTP_200_OK
                )
            else :
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
            


class UserProfileView(APIView):
    renderer_classes = [renderers.UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = serializers.UserProfileSerializer(request.user) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserChangePasswordView(APIView):
    renderer_classes = [renderers.UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.UserChangePasswordSerializerNew(
            data=request.data,
            context={'user': request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    'msg':'Change of Password Is Successful !'
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  





class SendPasswordResetEmailView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, format=None):
        serializer = serializers.SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    'msg':'Reset Password link Has Been Sent! Please, Check Your Email!'
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    


class UserPasswordResetView(APIView):
    renderer_classes = [renderers.UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = serializers.UserPasswordResetSerializer(
            data=request.data,
            context={'uid':uid, 'token': token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {
                    'msg':'Reset of Password Is Successfull!'
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
def index(request):
    return render(request, 'index.html')