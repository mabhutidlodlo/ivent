
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog
from .consumer import NotificationConsumer

@receiver(post_save, sender =Blog )

def create_new_blog(sender, created, instance, **kwargs):

    if created:

        NotificationConsumer.receive(instance.author.username)
