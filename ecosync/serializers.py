from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import CustomUser as User
from django.core.mail import send_mail



from django.core.mail import send_mail, BadHeaderError
import os
from dotenv import load_dotenv
load_dotenv()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    



class UseLogInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta: 
        model = User
        fields = ['username', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        style={'input_type':'password'},
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=255,
        style={'input_type':'password'},
        write_only=True
    )
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password == password2:
            user.set_password(password)
            user.save()
            return data
        raise serializers.ValidationError("Password and Confirm Password Did Not Match!")
    

class UserChangePasswordSerializerNew(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )
    new_password = serializers.CharField(
        max_length=255,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.context.get('user')

        if not check_password(old_password, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        if old_password == new_password:
            raise serializers.ValidationError("New password must be different from old password.")
        user.set_password(new_password)
        user.save()
        return data
    



class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        else:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:5173'+'/auth/reset-password/'+uid+'/'+token+'/'
            print(link)
            # S E N D   E M A I L 
            body = 'Hello, '+user.first_name+' '+user.last_name+' 😁\n\n'+'Click the following link to reset your password: \n'+link+'\n\nToken Endpoint: \n/'+uid+'/'+token+'/\n\nNote: This link will be valid for 15 mins till the email has been sent!'
            data = {
                'body': body,
                'subject': 'DJANGO AUTH | Reset Your Password',
                'to_email':user.email
            }
            #Util.send_email(data)
            send_mail(data['subject'],data['body'],os.environ.get('EMAIL_USER'),[data['to_email']])
            return data
            
        

class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        style={'input_type':'password'},
        write_only=True
    )
    class Meta:
        model = User
        fields = ['password']

    def validate(self, data):
        try:
            password = data.get('password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token Is Not Valid Or Expired!!')
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator(user, token)
            raise serializers.ValidationError('Token Is Not Valid Or Expired!!') 
            