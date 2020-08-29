from django.urls import path,include
from .views import (User,Profile,PostAPIView,
                    UserPosts,Search,FollowerAPIView,
                    FollowingAPIView,FeedAPIView,StartFollowAPIView,
                    StopFollowAPIView,UniqueEmailCheck,UniqueUsernameCheck,
                    Register,
                    UpdatePicAPIView,Profile_Detail)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('users/', User.as_view(),name="users"),
    path('rest-auth/',include("rest_auth.urls")),
    path('api-auth/',include("rest_framework.urls")),
    path("profile/<str:usrname>",Profile.as_view(),name="profile-detail"),
    path("create-post",PostAPIView.as_view(),name="postapi"),
    path("post/<int:pk>",PostAPIView.as_view(),name="single-post"),
    path("post/<int:pk>/edit",PostAPIView.as_view(),name="post-edit"),
    path("profile/<str:username>/posts",UserPosts.as_view(),name="user-posts"),
    path("search",Search.as_view(),name="search"),
    path("profile/<str:username>/followers",FollowerAPIView.as_view(),name="followers"),
    path("profile/<str:username>/following",FollowingAPIView.as_view(),name="following"),
    path("gethomefeed",FeedAPIView.as_view(),name="home-feed"),
    path("addfollow/<str:profile_username>",StartFollowAPIView.as_view(),name="start-follow"),
    path("removefollow/<str:profile_username>",StopFollowAPIView.as_view(),name="stop-follow"),
    path("doesemailexist",UniqueEmailCheck,name="check-email"),
    path("doesusernameexist",UniqueUsernameCheck,name="username-check"),
    path("register",Register,name="my-register"),
    # path("testing",csrf_exempt(Image.as_view()),name="dhgtd"),
    path("update-pic",UpdatePicAPIView.as_view(),name="update-pic"),
    path("profile-detail",Profile_Detail,name="profile-detail"),
]