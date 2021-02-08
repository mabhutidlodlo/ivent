
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','first_name', 'last_name']

    def create (self, validated_data,*args, **kwargs):
        user = User(username = validated_data['username'],first_name = validated_data['first_name'],last_name = validated_data['last_name'],)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        def validate(self, attrs):
            username = attrs.get("username")
            password = attrs.get("password")
            if len(username)>0 and len(password)> 0:
                user = authenticate(username=username, password=password)

            else:
                raise serializers.ValidationError("make sure all fields are field")
                
            if user:
                attrs["user"] = user
                return attrs
            else:
                raise serializers.ValidationError(
                "Unable to login with credentials provided."
                )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields = "__all__"

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields = ['id','avatar','about']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ["username"]
