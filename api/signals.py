from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .serializers import ProfileSerializer

from .models import Profile
import os, pathlib

# @receiver(post_save, sender=Profile)
# def after(sender, instance, created, **kwargs):
#     global FILE_PATH
#     os.remove(FILE_PATH)