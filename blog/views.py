from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Blog, Comment
from accounts.models import Profile
from accounts.serializer import ProfileSerializer
from .serializers import ArticleDetailSerializer,CommentDetailSerializer, BlogSerializer,PostBlogSerializer ,  CommentSerializer
# Create your views here.

class ListBlogs(ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.order_by("-date_created")
    serializer_class = BlogSerializer
    lookup_field = 'slug'

class CategoryBlogs(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, category):
        queryset = Blog.objects.order_by('-date_created').filter(category = category)
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)


class MyBlog(APIView):
    serializer_class = PostBlogSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.POST._mutable = True
        data = request.data
        data['author'] = request.user.id
        serializer = PostBlogSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"created new article"}, status = 201)
        return Response(serializer.errors, status = 400)

    def get(self, request, fomart=None):
        try:
            queryset = Blog.objects.order_by('date_created').filter(author = Profile.objects.get(user = request.user))
        except Blog.DoesNotExist:
            return Response({"no articles"}, status =404)
        serializer = BlogSerializer(queryset, many = True)
        return Response(serializer.data,content_type='image/*',status = 200)

class SubscribedArticles(APIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        articles = {}
        profiles = Profile.objects.get(id = request.user.id).following.all()
        for prof in profiles:
            article = Blog.objects.order_by('-date_created').filter(author =prof.id )
            articles=article
        serializer = BlogSerializer(articles, many=True)

        return Response(serializer.data, status = 200)

class Blogs(APIView):
    serializer_class = BlogSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            queryset = Blog.objects.get(slug = slug)
        except ObjectDoesNotExist:
            return Response({"The article does not exist it may be deleted"})

        serializer = ArticleDetailSerializer(Blog.objects.get(slug=slug))
        return Response(serializer.data,content_type='image/*', status = 200)

    def put(self,request, slug):
        try:
            queryset = Blog.objects.get(slug = slug)
        except Blog.DoesNotExist:
            return Response({"article does not exist it may be deleted"}, status = status.HTTP_404_NOT_FOUND
)
        request.POST._mutable = True
        data = request.data
        if data['pic'] == queryset.pic.url:
            data['pic'] = queryset.pic
        data['author'] = request.user.id
        serializer = PostBlogSerializer(queryset,data = data )
        if serializer.is_valid():
            serializer.save()

            return Response({"message":"article succesefully updated"},status=201)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        try:
            queryObject = Blog.objects.get(slug = slug)
        except Blog.DoesNotExist:
            return Response({"article does not exist, it may be deleted"}, status = 404)

        if queryObject.author.id == request.user.id:
            queryObject.delete()
            return Response({"article successfully deleted"},status=200)

        return Response({"dont have privilage to delete"},status = 400)

class Claps(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            queryObject = Blog.objects.get(slug = slug)
        except Blog.DoesNotExist:
            return Response({"article does not exist"})

        if queryObject.claps.filter(id = request.user.id).exists():
            queryObject.claps.remove(request.user)
            claped = False
            num_claps = queryObject.claps_count()
        else:
            queryObject.claps.add(request.user)
            claped = True
            num_claps = queryObject.claps_count()

        comments = Comment.objects.filter(article = queryObject.id).count()

        return Response({"claped":claped , "num_claps": num_claps, "comments":comments},status = 200)

    def get(self,request, slug):
        try:
            queryObject = Blog.objects.get(slug = slug)
        except Blog.DoesNotExist:
            return Response({"article does not exist"},status = 404)
        claped = False
        if queryObject.claps.filter(id= request.user.id).exists():
            claped = True
        data = {"user_clapped":claped, "num_claps": queryObject.claps_count()}

        return Response(data,status =200)

class Comments(APIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        request.POST._mutable = True
        data = request.data
        data['author']= request.user.id
        data['article'] = Blog.objects.get(slug = slug).id
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"comment created"}, status= 201)
        return Response(serializer.errors)

    def get(self, request, slug):
        article = Blog.objects.get(slug__exact=slug)
        try:
            queryset = Comment.objects.order_by('-date_created').filter(article = article)
        except Comment.DoesNotExist:
            return Response({"no comments"})
        serializer = CommentDetailSerializer(queryset, many = True)
        return Response(serializer.data, status = 200)


class MyComment(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request, pk):
        try:
            queryset = Comment.objects.get(id = pk)
        except Comment.DoesNotExist:
            return Response({"comment does not exist it may be deleted"}, status = 404)

        request.POST._mutable = True
        data = request.data
        data['author'] = request.user.id
        serializer = CommentSerializer(queryset,data = data )
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"succesfully updated"}, status = 201)
        return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            queryObject = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"comment does not exist, it may be deleted"}, status = 404)

        if queryObject.author == request.user:
            queryObject.delete()
            return Response({"message":"comment successfully deleted"},status = 200)

        return Response({"dont have privilage to delete"},status =400)

class GetAuthor(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        author = Blog.objects.get(slug=slug).author
        try:
            set = Profile.objects.filter(id=author.id)
        except Profile.DoesNotExist:
            return Response({"message":"article does not exist"},status =404)

        serializer = ProfileSerializer(set, many=True)
        return Response(serializer.data, status =200)
