from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .serializers import ProfileSerializer

from .models import Profile

def get_url(instance):
    # print(instance)
    obj = Profile.objects.filter(id=instance.id).first()
    # print(obj)
    if obj is None:
        print("Something is wrong")
    serializer = ProfileSerializer(obj)
    # print(serializer.data)
    url = "https://pubgapi.pythonanywhere.com/"+serializer.data.get("profile_pic")
    return url

@receiver(pre_save, sender=Profile)
def update_or_create_avatar_link(sender, instance, created, **kwargs):
    print(instance.profile_pic.path)

@receiver(post_save, sender=Profile)
def update_or_create_avatar_link(sender, instance, created, **kwargs):
    print(instance.profile_pic.path)