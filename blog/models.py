from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from accounts.models import Profile
# Create your models here.

class Categories(models.TextChoices):
    CULTURE = 'culture'
    FOOD = 'food'
    HEALTH = 'health'
    MEDIA = 'media'
    OPINION = 'opinion'
    PROGRAMING = 'programing'
    WORLD = 'world'
    SPORT = 'sport'


class Blog (models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    title =  models.CharField(max_length = 100)
    slug = models.SlugField()
    category = models.CharField(max_length = 100, choices = Categories.choices, default = Categories.SPORT)
    pic = models.ImageField(upload_to = 'pictures/%y/%m/%d')
    hint = models.CharField(max_length =100)
    content = models.TextField()
    featured = models.BooleanField(default = False)
    pic_name = models.CharField(max_length=100)
    claps = models.ManyToManyField(User, related_name= "blog_claps", blank=True)
    date_created = models.DateTimeField(default = datetime.now, blank = True)

    def claps_count(self, *args, **kwargs):
        return self.claps.count()

    def save(self, *args, **kwargs):
        first_slug = slugify(self.title)
        queryset = Blog.objects.all().filter(slug__iexact=first_slug).count()
        i = 1
        slug = first_slug
        while(queryset):
            slug = first_slug + "_" + str(i)
            queryset = Blog.objects.all().filter(slug__iexact=slug).count()
            i +=1

        self.slug = slug

        if self.featured:
            try:
                temp = Blog.objects.get(featured = True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Blog.DoesNotExist:
                pass

        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Blog, on_delete = models.CASCADE)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    body = models.CharField(max_length = 500)
    date_created = models.DateTimeField(default =datetime.now)

    def __str__(self):
        return self.article.title