import sys
sys.path.append("/my_blog")
from rest_framework import serializers
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from .models import Blog ,  Comment 
from accounts.models import Profile
from accounts.serializer import ProfileSerializer
# Serializers define the API representation.
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        lookup_field = 'slug'

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True)
    class Meta:
        model = Blog
        fields = '__all__'
        lookup_field = 'slug'

class PostBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title','author', 'pic_name','category','hint','content','pic']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Comment
        fields = ['id','body', 'author', 'article']

class CommentDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True)
    class Meta:
        many = True
        model = Comment
        fields = ['id','body', 'author', 'article']