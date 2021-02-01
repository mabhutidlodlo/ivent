from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions
from .serializer import UserSerializer ,UserEditSerializer ,LoginSerializer, EditProfileSerializer , ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authtoken.models import Token
from .models import Profile
from blog.models import Blog
from blog.models import Comment
from rest_framework.parsers import MultiPartParser,FormParser

# Create your views here.

class NewUser(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request, format = None):
        data = request.data
        serializer  = UserSerializer(data =data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        if user:
            token = Token.objects.create(user = user)

            return Response(serializer.data)

        return Response(serializer.errors)

class Login(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request, format = None):
        data = request.data
        serializer = LoginSerializer(data =data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data['username'])
            profile = Profile.objects.get(user = user.id)
            token = Token.objects.get(user=user)
            response = {}
            response['user'] = serializer.data
            response['token'] = token.key
            response['profile']=ProfileSerializer(profile).data
            return Response(response)
        return Response(serializer.errors)

class AddUser(APIView):
    serializer_class = UserEditSerializer
    permission_classes = [permissions.AllowAny]

    def put(self, request):

        try:
            user = User.objects.get(id=request.user.id)

        except UserDoesNotExist:
            return Response({"mesage":"user does not exist"})

        request.POST._mutable = True
        serializer = UserEditSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status = 400)

class MyProfile(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes =[MultiPartParser,FormParser]
    def put(self, request,format=None):
        try:
            set = Profile.objects.get(user = request.user.id)
        except Profile.DoesNotExist:
            return Response({"message":"profile does not exist"})
        request.POST._mutable = True

        request.data['user'] = request.user.username
        if request.data['avatar'] == set.avatar.url:
           request.data['avatar'] =set.avatar
           print(request.data)
        serializer = EditProfileSerializer(set, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)

        return Response(serializer.errors, status = 400)


    def get(self, request):
        try:
            profile = Profile.objects.get(user = request.user.id)

        except Profile.DoesNotExist:
            return Response({'profile does not exist'}, status = 404)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class Follow(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request,id):
        try:
            profile = Profile.objects.get(id = id)

        except Profile.DoesNotExist:
            return Response('profile not found', status = 404)

        following = False
        num_followers = 0
        if profile.followers.filter(id = request.user.id).exists():
            profile.followers.remove(request.user)

        else :
            profile.followers.add(request.user)
            following = True

        num_followers = profile.followers.count()

        return Response({'num_followers':num_followers, 'following':following})



class Info(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get(self,request,id):
        try:
            profile= Profile.objects.get(id = id)

        except Profile.DoesNotExist:
            return Response({'message':'profile doesnt exist'})

        posts = Blog.objects.filter(author = profile.id)
        num_post = posts.count()
        average_likes= 0
        num_comments = 0
        likes =0
        CommentS=0
        for post in posts:
            likes = post.claps.all().count()+ likes
            comments = Comment.objects.filter(article=post.id).count()
            average_likes =average_likes + likes
            num_comments = num_comments + comments

        num_followers = profile.followers.count()
        following = False
        if profile.followers.filter(id = request.user.id).exists():
            following = True


        serializer = ProfileSerializer(profile)
        response = {}
        response['average_likes'] = average_likes
        response['num_post'] =  num_post
        response['num_followers'] =  num_followers
        response['following'] =  following
        response['comments'] =  num_comments
        response['profile'] = serializer.data
        return Response(response, status = 200)
