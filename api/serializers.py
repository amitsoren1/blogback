from rest_framework import serializers
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from .models import ExampleModel,Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username","email","password")
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        try:
            UserModel = get_user_model()
            user = UserModel(username=validated_data.get("username"),
                                 email=validated_data.get('email'))
            user.set_password(validated_data.get("password"))
            user.save()
            return user
        except IntegrityError as error:
            return {"data":False}

# class MySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExampleModel
#         fields = ("model_pic",)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'