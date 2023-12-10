from django.db import models
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save
import os


# @receiver(post_save, sender=Video)
# def generate_thumbnail_on_post_save(sender, instance, **kwargs):
#     if not instance.thumbnail:
#         instance.save()
