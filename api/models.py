from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from PIL import Image
import os
from django.conf import settings

def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    print(f"/pic_folder/{instance.user.username}{file_extension}")
    if os.path.exists(f"./pic_folder/{instance.user.username}/{instance.user.username}{file_extension}"):
        import shutil
        shutil.rmtree(os.path.join(settings.BASE_DIR, f"pic_folder/{instance.user.username}"))
        print("SSSSSSSSSSSSSSSSSS")
        # os.remove(path = os.path.join(settings.BASE_DIR, "temp12"))#f"./pic_folder/{instance.user.username}{file_extension}")
    else:
        print("Folder may not exist")
    return f'pic_folder/{instance.user.username}/{instance.user.username}{file_extension}'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField('Profile', related_name='followed_by',blank=True)
    profile_pic = models.ImageField(upload_to =photo_path , default = 'pic_folder/default.png')

    '''def save(self, *args, **kwargs):
        super(Profile,self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)'''

    def __str__(self):
        return f"{self.user.username}"

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="posts")
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to = 'pic_folder/amit/', default = 'pic_folder/None/no-img.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.model_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.model_pic.path)