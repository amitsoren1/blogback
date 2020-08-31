from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .serializers import ProfileSerializer

from .models import Profile
import os, pathlib

FILE_PATH = ""

def get_url(instance):
    file_name = instance.profile_pic.path.split("/")[-1]
    url = "https://pubgapi.pythonanywhere.com/"+"media/pic_folder/"+f"{profile.user.username}/"+file_name
    return url

@receiver(post_save, sender=Profile)
def after(sender, instance, created, **kwargs):
    global FILE_PATH
    print(FILE_PATH)