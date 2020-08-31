from django.db.models.signals import post_save
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

# @receiver(post_save, sender=Profile)
# def update_or_create_avatar_link(sender, instance, created, **kwargs):
#     url = get_url(instance)
#     print(url)
#     import requests
#     pload = {'username':instance.user.username,'avatar':url}
#     try:
#         r = requests.post('http://127.0.0.1:5000/update-pic',data = pload)
#         print(r)
#     except:
#         pass
#     # print(r.text)
#     # pass