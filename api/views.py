from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Post
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.decorators import api_view
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import UpdatePicSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
# Create your views here.
from .utils import get_url

class User(APIView):
    serializer_class = UserSerializer
    UserModel = get_user_model()
    queryset = UserModel.objects.all()
    def get(self, request, format=None):
        snippets = self.UserModel.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPosts(APIView):
    def get(self,request,username):
        posts = Post.objects.filter(author__user__username=username)
        res = []
        for post in posts:
            newpost = {}
            newpost["_id"] = post.id
            newpost["author"] = {"avatar":get_url(post.author)}
            newpost["title"] = post.title
            newpost["createdDate"] = [post.created_on.year,post.created_on.month-1,post.created_on.day]
            res.append(newpost.copy())
        return Response(res)

class Profile(APIView):
    def post(self,request,usrname,format=None):
        user1 = Token.objects.filter(key=request.data.get("token")).first().user
        if user1 is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        UserModel = get_user_model()
        user = UserModel.objects.filter(username=usrname).first()
        isFollowing = user.profile.followed_by.filter(user=user1)
        if user is not None:
            response = {
                "profileUsername": user.username,
                "profileAvatar": get_url(user.profile),
                "isFollowing": False,
                "counts": {
                    "postCount": user.profile.posts.all().count(),
                     "followerCount": user.profile.followed_by.all().count(),
                      "followingCount": user.profile.follows.all().count() 
                    },
                "isFollowing":bool(isFollowing)
                }
            return Response(response)
        else:
            return Response({"gh":45})

class PostAPIView(APIView):
    def get(self,request,pk):
        obj = Post.objects.filter(id=pk).first()
        return Response({"_id":obj.id,"title":obj.title,"body":obj.body,
                        "createdDate": [obj.created_on.year,obj.created_on.month-1,obj.created_on.day],
                        "author":{
                            "username":obj.author.user.username,
                            "avatar":get_url(obj.author)
                            }
                        }
                    )

    def post(self,request):
        # print("HHHHHHHHHH")
        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        obj = Post(title=request.data.get("title"),
                    body=request.data.get("body"),
                    author=user.profile
                    )
        obj.save()
        obj2 = Post.objects.filter(title=request.data.get("title"),
                                    body=request.data.get("body"),
                                    author=user.profile).first()
        return Response({"id":obj2.id})
    
    def put(self,request,pk):
        if request.data.get("method") == "delete":
            post = Post.objects.get(id=pk)
            if post is None:
                return Response({"bad":"request"},status=status.HTTP_404_NOT_FOUND)
            user = Token.objects.filter(key=request.data.get("token")).first().user
            if user is None:
                return Response({"credentials":"wrong"},status=status.HTTP_403_FORBIDDEN)
            if user.profile == post.author:
                post.delete()
            return Response({"message":"Success"})

        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        obj = Post.objects.filter(id=pk).first()
        if obj is None:
            return Response({"bad":"request"},status=status.HTTP_404_NOT_FOUND)
        obj.title = request.data.get("title")
        obj.body = request.data.get("body")
        obj.save()
        return Response({"title":obj.id,"body":obj.body,
                        "author":{"username":obj.author.user.username}})
    
    # def delete(self,request,pk):
    #     # print(request.data)
    #     post = Post.objects.get(id=pk)
    #     if post is None:
    #         return Response({"bad":"request"},status=status.HTTP_404_NOT_FOUND)
    #     user = Token.objects.filter(key=request.data.get("token")).first()#.user
    #     # if user is None:
    #         # return Response({"credentials":"wrong"},status=status.HTTP_403_FORBIDDEN)
    #     # if user.profile == post.author:
    #     #     post.delete()
    #     return Response({"message":"Success"})

class Search(APIView):
    def post(self,request):
        posts = Post.objects.filter(Q(title__contains=request.data.get("searchTerm")) | Q(body__contains=request.data.get("searchTerm")))
        res = []
        for post in posts:
            newpost = {}
            newpost["_id"] = post.id
            newpost["author"] = {"avatar":get_url(post.author)}
            newpost["title"] = post.title
            newpost["createdDate"] = [post.created_on.year,post.created_on.month-1,post.created_on.day]
            res.append(newpost.copy())
        return Response(res)

class FollowerAPIView(APIView):
    def get(self,request,username):
        from .models import Profile
        profile = Profile.objects.get(user__username=username)
        profiles = profile.followed_by.all()
        res = []
        for profile in profiles:
            newprofile = {}
            newprofile["username"] = profile.user.username
            newprofile["avatar"] = get_url(profile)
            # newprofile["createdDate"] = [post.created_on.year,post.created_on.month-1,post.created_on.day]
            res.append(newprofile.copy())
        return Response(res)

class FollowingAPIView(APIView):
    def get(self,request,username):
        from .models import Profile
        profile = Profile.objects.get(user__username=username)
        profiles = profile.follows.all()
        res = []
        for profile in profiles:
            newprofile = {}
            newprofile["username"] = profile.user.username
            newprofile["avatar"] = get_url(profile)
            # newprofile["createdDate"] = [post.created_on.year,post.created_on.month-1,post.created_on.day]
            res.append(newprofile.copy())
        return Response(res)

class FeedAPIView(APIView):
    def post(self,request):
        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        profiles = user.profile.follows.all()
        res = []
        for profile in profiles:
            for post in profile.posts.all().order_by('-created_on'):
                newpost = {}
                newpost["_id"] = post.id
                newpost["title"] = post.title
                newpost["createdDate"] = [post.created_on.year,post.created_on.month-1,post.created_on.day]
                newpost["author"] = {"username":post.author.user.username,
                                    "avatar":get_url(post.author)}
                res.append(newpost.copy())
        return Response(res)

class StartFollowAPIView(APIView):
    def post(self,request,profile_username):
        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        from .models import Profile
        profile = Profile.objects.get(user__username=profile_username)
        user.profile.follows.add(profile)
        return Response({"following":True})

class StopFollowAPIView(APIView):
    def post(self,request,profile_username):
        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        from .models import Profile
        profile = Profile.objects.get(user__username=profile_username)
        user.profile.follows.remove(profile)
        return Response({"following":False})

@api_view(['POST'])
def UniqueEmailCheck(request):
    if request.method == 'POST':
        User = get_user_model() 
        user = User.objects.filter(email=request.data.get("email")).first()
        message = "false"
        if user is None:
            message = "true"
        return Response({"message": message})

@api_view(['POST'])
def UniqueUsernameCheck(request):
    if request.method == 'POST':
        User = get_user_model()
        user = User.objects.filter(username=request.data.get("username")).first()
        message = "false"
        if user is None:
            message = "true"
        return Response({"message": message})

@api_view(['POST'])
def Register(request):
    if request.method == 'POST':
        credentials = {"username":request.data.get("username"),
                        "email":request.data.get("email"),
                        "password":request.data.get("password"),
                        }
        # response = requests.post("http://pubgapi.pythonanywhere.com/users/",data=credentials)
        # response_data = response.json()
        User = get_user_model()
        # user = User.objects.filter(username=response_data["username"]).first()
        user = User.objects.create(username=credentials["username"],email=credentials["email"])
        user.set_password(credentials["password"])
        user.save()
        credentials = {"username":request.data.get("username"),"password":request.data.get("password")}
        token = Token.objects.filter(user=user).first()
        if token is None:
            token = Token.objects.create(user=user)
        # response = requests.post("http://pubgapi.pythonanywhere.com/rest-auth/login/",data=credentials)
        response_data = {}
        # print(user)
        response_data["username"] = user.username
        response_data["token"] = token.key
        from .models import Profile
        profile = Profile(user=user)
        profile.save()
        response_data["avatar"] = get_url(profile)
        return Response(response_data)

# class UpdatePicAPIView(APIView):
#     def post(self, request, format=None):
#         # print(type(request.data.get("token")))
#         image = request.data["model_pic"]
#         token = request.data.get("token")
#         user = Token.objects.filter(key=request.data.get("token")).first().user
#         if user is None:
#             return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
#         # print(bool(t))
#         from .models import Profile
#         profile = Profile.objects.filter(user=user).update(profile_pic=image)
#         # profile.profile_pic = image
#         # profile.save()
#         # serializer = MySerializer(data=request.data)
#         # if serializer.is_valid():
#             # serializer.save()
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({"updated":True})#serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from braces.views import CsrfExemptMixin
# class Image(APIView):
#     permission_classes = []
#     queryset = ExampleModel.objects.all()
#     serializer_class = MySerializer
#     def get(self, request, format=None):
#         snippets = ExampleModel.objects.all()
#         serializer = MySerializer(snippets, many=True)
#         obj = ExampleModel.objects.first()
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         t=request.data["model_pic"]
#         print(request.data)
#         image = ExampleModel.objects.all().first()#create(model_pic=t)
#         image.model_pic = t
#         image.save()
#         # serializer = MySerializer(data=request.data)
#         # if serializer.is_valid():
#             # serializer.save()
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({"gvhv":"fcgc"})#serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

# def pics(request):
#     return render(request,)user.profile.image.url
from django.http import HttpResponse

# def Image(request):
#     with open('file.csv', 'r') as file:
#         response = HttpResponse(file, content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename=file.csv'
#     return response

@api_view(['POST'])
def Profile_Detail(request):
    if request.method == 'POST':
        credentials = {"username":request.data.get("username"),
                        "password":request.data.get("password"),
                        }
        user = authenticate(username=credentials["username"], password=credentials["password"])
        # print(user)
        # User = get_user_model()
        # temp_user = User(username="temp",email="temp@email.com")
        # temp_user.set_password(credentials["password"])
        # user = User.objects.filter(username=credentials["username"]).first()
        # print(user.password,temp_user.password)
        token = Token.objects.filter(user=user).first()
        # response = requests.post("http://pubgapi.pythonanywhere.com/rest-auth/login/",data=credentials)
        if token is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)       
        # response_data = response.json()
        response = {}
        response["token"] = token.key
        # user = Token.objects.filter(key=response_data["key"]).first().user
        response["username"] = user.username
        response["avatar"] = get_url(user.profile)
        # print(response)
        return Response(response)

class UpdatePicAPIView(APIView):
    from .models import Profile
    serializer_class = UpdatePicSerializer
    queryset = Profile.objects.all()
    def post(self,request):
        # print(request.data)
        token = request.data.get("token")
        user = Token.objects.filter(key=request.data.get("token")).first().user
        if user is None:
            return Response({"credentials":"wrong"},status=status.HTTP_401_UNAUTHORIZED)
        # serializer = UpdatePicSerializer(user.profile,data=request.data)
        # if serializer.is_valid():
            # serializer.save()
            # return redirect(f"http://127.0.0.1:3000/profile/{user.username}")
            # return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("profile_pic") == None:
            return Response({"error":"no image sent"},status=status.HTTP_400_BAD_REQUEST)
        profile.profile_pic = request.data.get("profile_pic")
        profile.save()
        return Response({"avatar":get_url(profile)})
