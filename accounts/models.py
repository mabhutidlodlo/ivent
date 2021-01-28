from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(default = '/profile/avatar.png', upload_to = 'media/profile')
    username = models.CharField(max_length = 100)
    about = models.CharField(max_length = 300, null = True,  blank = True)

    def save(self, *args, **kwargs):
        self.username = User.objects.get(id = self.user.id).username
        super(Profile, self).save(*args, **kwargs)



    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()