"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path


from final_api.views import test, register, checkuser, logmein, getuser, post, getHomePosts
from final_api.views import getExplorePosts, getuserbyid, getUsersPosts, like, unlike
from final_api.views import getPost, getResponsePosts, removepost, postresponse, follow
from final_api.views import unfollow, getUsersFollowing, getUsersFollowed, editprofile
from final_api.views import postsearch, usersearch, getLikedPosts, getResponseToYou

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test.as_view(), name='test'),
    path('register/', register.as_view(), name='register'),
    path('checkuser/', checkuser.as_view(), name='checkuser'),
    path('logmein/', logmein.as_view(), name='logmein'),
    path('getuser/', getuser.as_view(), name='getuser'),
    path('post/', post.as_view(), name='post'),
    path('getHomePosts/', getHomePosts.as_view(), name='getHomePosts'),
    path('getExplorePosts/', getExplorePosts.as_view(), name='getExplorePosts'),
    path('getuserbyid/', getuserbyid.as_view(), name='getuserbyid'),
    path('getUsersPosts/', getUsersPosts.as_view(), name='getUsersPosts'),
    path('like/', like.as_view(), name='like'),
    path('unlike/', unlike.as_view(), name='unlike'),
    path('getPost/', getPost.as_view(), name='getPost'),
    path('getResponsePosts/', getResponsePosts.as_view(), name='getResponsePosts'),
    path('removepost/', removepost.as_view(), name='removepost'),
    path('postresponse/', postresponse.as_view(), name='postresponse'),
    path('postresponse/', postresponse.as_view(), name='postresponse'),
    path('follow/', follow.as_view(), name='follow'),
    path('unfollow/', unfollow.as_view(), name='unfollow'),
    path('getUsersFollowing/', getUsersFollowing.as_view(), name='getUsersFollowing'),
    path('getUsersFollowed/', getUsersFollowed.as_view(), name='getUsersFollowed'),
    path('editprofile/', editprofile.as_view(), name='editprofile'),
    path('postsearch/', postsearch.as_view(), name='postsearch'),
    path('usersearch/', usersearch.as_view(), name='usersearch'),
    path('getLikedPosts/', getLikedPosts.as_view(), name='getLikedPosts'),
    path('getResponseToYou/', getResponseToYou.as_view(), name='getResponseToYou'),

]