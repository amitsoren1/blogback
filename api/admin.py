from django.contrib import admin
from .models import Post,Profile,ExampleModel
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(ExampleModel)