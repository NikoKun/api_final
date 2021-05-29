from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout


from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context
from django.template.defaultfilters import pprint
from django.urls import reverse
from django.views.generic.base import View

from django.http import JsonResponse

from final_api.models import UserInfo, Post, Like, Follow, User

import json 
import os

import base64
from uuid import uuid4
from datetime import date
# django-cors-headers


class test(View):
    def get(self, request):

        data = { 'name': 'NikoKun', 'image': 'img1.jpg', 'verified': True, 'text': 'Increible Tweet'} 

        return JsonResponse(data, safe=False)



class getHomePosts(View):
    def post(self, request):
        tokenData = str(request.body)[2:-1]
        user_info = UserInfo.objects.filter(token=tokenData).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.all().order_by('-publish_date')
            allfollows = Follow.objects.filter(id_user_folloing = user_info.id_user.id)

            for postTMP in allposts:
                for followTMP in allfollows:
                    if postTMP.writer.id != user_info.id_user.id:
                        if postTMP.writer.id == followTMP.id_user_followed.id or postTMP.writer.id == user_info.id_user.id:

                            user_followed = User.objects.filter(id = postTMP.writer.id).first()        
                            user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                            like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                            likes = Like.objects.filter(id_post = postTMP)
                            replies = Post.objects.filter(in_response = postTMP.id)

                            if like is not None: 
                                info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                dataToPost.append(info)
                            else:
                                info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                dataToPost.append(info)

                            break

                if postTMP.writer.id == user_info.id_user.id:

                    user_followed = User.objects.filter(id = postTMP.writer.id).first()        
                    user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                    like = Like.objects.filter(id_user = postTMP.writer, id_post = postTMP).first()    
                    likes = Like.objects.filter(id_post = postTMP)
                    replies = Post.objects.filter(in_response = postTMP.id)

                    if like is not None: 
                        info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                        dataToPost.append(info)
                    else:
                        info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                        dataToPost.append(info)

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)




class getExplorePosts(View):
    def post(self, request):
        tokenData = str(request.body)[2:-1]
        user_info = UserInfo.objects.filter(token=tokenData).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.all().order_by('-publish_date')
            allfollows = User.objects.all()
                
            for postTMP in allposts:
                for followTMP in allfollows:
                    if postTMP.writer.id == followTMP.id:

                        user_followed = User.objects.filter(id = followTMP.id).first()        
                        user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                        like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                        likes = Like.objects.filter(id_post = postTMP)
                        replies = Post.objects.filter(in_response = postTMP.id)

                        if like is not None: 
                            info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                            dataToPost.append(info)
                        else:
                            info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                            dataToPost.append(info)
                        break

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)



class getLikedPosts(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user_req_info = UserInfo.objects.filter(id_user=data['iduser']).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.all().order_by('-publish_date')
            allfollows = User.objects.all()

            for postTMP in allposts:
                for followTMP in allfollows:
                    if postTMP.writer.id == followTMP.id:

                        user_followed = User.objects.filter(id = followTMP.id).first()        
                        user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                        like = Like.objects.filter(id_user = user_req_info.id_user, id_post = postTMP).first()    
                        likes = Like.objects.filter(id_post = postTMP)
                        replies = Post.objects.filter(in_response = postTMP.id)

                        if like is not None: 
                            info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                            dataToPost.append(info)

                        break
                        
            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)




class getResponseToYou(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user_req_info = UserInfo.objects.filter(id_user=data['iduser']).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.all().order_by('-publish_date')
            allfollows = User.objects.all()

            for postTMP in allposts:
                if postTMP.in_response is not None:
                    posrresponded = Post.objects.filter(id=postTMP.in_response).first()
                    if posrresponded.writer.id == user_req_info.id_user.id:
                        for followTMP in allfollows:
                            if postTMP.writer.id == followTMP.id:

                                user_followed = User.objects.filter(id = followTMP.id).first()        
                                user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                                like = Like.objects.filter(id_user = user_req_info.id_user, id_post = postTMP).first()    
                                likes = Like.objects.filter(id_post = postTMP)
                                replies = Post.objects.filter(in_response = postTMP.id)

                                if like is not None: 
                                    info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                    dataToPost.append(info)
                                else:
                                    info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                    dataToPost.append(info)
                                break
                        
            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)










class postsearch(View):
    def post(self, request):
        search = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=search['token']).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.all().order_by('-publish_date')
            allfollows = User.objects.all()
                    
            for postTMP in allposts:
                user_search = User.objects.filter(id=postTMP.writer.id).first()

                if search['searchabar'].upper() in postTMP.body.upper() or search['searchabar'].upper() in user_search.username.upper() or search['searchabar'].upper() in user_search.first_name.upper() or search['searchabar'].upper() in user_search.last_name.upper():
                    for followTMP in allfollows:
                        if postTMP.writer.id == followTMP.id:

                            user_followed = User.objects.filter(id = followTMP.id).first()        
                            user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                            like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                            likes = Like.objects.filter(id_post = postTMP)
                            replies = Post.objects.filter(in_response = postTMP.id)

                            if like is not None: 
                                    info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                    dataToPost.append(info)
                            else:
                                    info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                    dataToPost.append(info)
                            break

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)






class usersearch(View):
    def post(self, request):
        search = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=search['token']).first()

        if user_info is not None:
            dataToPost = list()
            allusers = User.objects.all()
                    
            for user_search in allusers:
                if search['searchabar'].upper() in user_search.username.upper() or search['searchabar'].upper() in user_search.first_name.upper() or search['searchabar'].upper() in user_search.last_name.upper():
                    user = user_search
                    user_info_following = UserInfo.objects.filter(id_user=user.id).first()

                    following = Follow.objects.filter(id_user_folloing=user.id)
                    your_followers = Follow.objects.filter(id_user_followed=user.id)
                    
                    follow =  Follow.objects.filter(id_user_folloing=user_info.id_user.id, id_user_followed=user.id)
                    followQuestion = 0

                    if len(follow) is not 0:
                        followQuestion = 1
                    if user_info.id_user.id is user.id:
                        followQuestion = 2

                    datatoapend = {
                        "id": user.id,
                        "username": user.username,
                        "is_superuser": user.is_superuser,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "img": user_info_following.img,
                        "desc": user_info_following.desc,
                        "following": str(len(following)),
                        "your_followers": str(len(your_followers)),
                        "followQuestion": followQuestion,
                    }
                    dataToPost.append(datatoapend)



            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)












class register(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if data['username'] is not None and data['username'] is not '':
            if len(data['username']) > 3 and len(data['username']) < 21 is not '':
                if data['email'] is not None and data['email'] is not '':
                    if data['password'] is not None and data['password'] is not '':
                        userRepe = User.objects.filter(username=data['username']).first()
                        if userRepe is None:
                            userRepe = User.objects.filter(email=data['email']).first()
                            if userRepe is None:

                                userTMP = User.objects.create(
                                    username = data['username'], 
                                    email = data['email'], 
                                    password = data['password'],
                                    first_name = data['firstname'],
                                    last_name = data['lastname'],
                                )

                                filename = ''
                                if 'image' in data:

                                    x = data['image'].split(",")
                                    imgdata = base64.b64decode(x[1])
                                    path = 'final_api/static/public/'
                                    filename = str(userTMP.id) + '_profilepic.png'
                                    endfilename = path + '' + filename
                                    with open(endfilename, 'wb') as f:
                                        f.write(imgdata)


                                UserInfo.objects.create(
                                    id_user = userTMP, 
                                    img = filename,
                                    desc = data['description'], 
                                    verified = 0, 
                                    public = 1,
                                    token = uuid4()
                                )

                                return JsonResponse(1, safe=False)
                            return JsonResponse('This email is already taken...', safe=False)
                        return JsonResponse('This username is already taken...', safe=False)
                    return JsonResponse('The password is required...', safe=False)
                return JsonResponse('The email is required...', safe=False)
            return JsonResponse('The username needs to be between 4 and 20 chars...', safe=False)
        return JsonResponse('The username is required...', safe=False)





class editprofile(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()


        if user_info is not None:
            user = User.objects.filter(id=user_info.id_user.id).first()

            if data['username'] is not None and data['username'] is not '':
                if len(data['username']) > 3 and len(data['username']) < 21 is not '':
                    if data['email'][0] is not None and data['email'][0] is not '':
                        userRepe = User.objects.filter(username=data['username']).first()
                        if userRepe.id == user_info.id_user.id:
                            userRepe = None

                        if userRepe is None:
                            userRepe = User.objects.filter(email=data['email'][0]).first()
                            if userRepe.id == user_info.id_user.id:
                                userRepe = None


                            if userRepe is None:
                                user.username = data['username']
                                user.email = data['email'][0]
                                user.first_name = data['firstname'][0]
                                user.last_name = data['lastname'][0]

                                if data['password'][0] != '':
                                    user.password = data['password'][0]


                                filename = ''
                                if 'image' in data:
                                    x = data['image'].split(",")
                                    imgdata = base64.b64decode(x[1])
                                    path = 'final_api/static/public/'
                                    filename = str(user.id) + '_profilepic.png'
                                    endfilename = path + '' + filename

                                    if os.path.exists(endfilename):
                                        os.remove(endfilename)

                                    with open(endfilename, 'wb') as f:
                                        f.write(imgdata)

                                user_info.desc = data['description'][0]
                                if filename != '':
                                    user_info.img = filename


                                user.save()
                                user_info.save()

                                return JsonResponse(1, safe=False)
                            return JsonResponse('This email is already taken...', safe=False)
                        return JsonResponse('This username is already taken...', safe=False)
                    return JsonResponse('The email is required...', safe=False)
                return JsonResponse('The username needs to be between 4 and 20 chars...', safe=False)
            return JsonResponse('The username is required...', safe=False)
        return JsonResponse('no', safe=False)




















class checkuser(View):
    def post(self, request):
        data = str(request.body)[2:-1]
        user = UserInfo.objects.filter(token=data).first()

        if user is not None:
            return JsonResponse(1, safe=False)
        return JsonResponse('This user does not exist... '+str(data), safe=False)




class logmein(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.filter(username=data['username_email'], password=data['password']).first()
        response = [{ 'response': 0, 'token': 'no', 'id': 'no'}]

        if user is not None:
            user_info = UserInfo.objects.filter(id_user=user.id).first()
            response = [{ 'response': 1, 'token': user_info.token, 'id': user_info.id_user.id}]
            return JsonResponse(response, safe=False)
        return JsonResponse('Username or password is incorrect.', safe=False)






class getuser(View):
    def post(self, request):
        tokenVar = str(request.body)[2:-1]
        user_info = UserInfo.objects.filter(token=tokenVar).first()

        if user_info is not None:
            user = User.objects.filter(id=user_info.id_user.id).first()

            following = Follow.objects.filter(id_user_folloing=user.id)
            your_followers = Follow.objects.filter(id_user_followed=user.id)


            dataToPost = {
                "username": user.username,
                "is_superuser": user.is_superuser,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "img": user_info.img,
                "desc": user_info.desc,
                "following": str(len(following)),
                "your_followers": str(len(your_followers)),
            }
            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)






class getUsersFollowing(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()
        following = Follow.objects.filter(id_user_folloing=data['iduser'])
        userrrr = User.objects.filter(id=data['iduser']).first()
        dataToPost = list()
        
        if user_info is not None:
            for user_following in following:
                user = User.objects.filter(id=user_following.id_user_followed.id).first()
                user_info_following = UserInfo.objects.filter(id_user=user.id).first()

                following = Follow.objects.filter(id_user_folloing=user.id)
                your_followers = Follow.objects.filter(id_user_followed=user.id)
                
                follow =  Follow.objects.filter(id_user_folloing=user_info.id_user.id, id_user_followed=user.id)
                followQuestion = 0

                if len(follow) is not 0:
                    followQuestion = 1
                if user_info.id_user.id is user.id:
                    followQuestion = 2

                datatoapend = {
                    "mainname": userrrr.username,
                    "id": user.id,
                    "username": user.username,
                    "is_superuser": user.is_superuser,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "img": user_info_following.img,
                    "desc": user_info_following.desc,
                    "following": str(len(following)),
                    "your_followers": str(len(your_followers)),
                    "followQuestion": followQuestion,
                }
                dataToPost.append(datatoapend)

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)





class getUsersFollowed(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()
        following = Follow.objects.filter(id_user_followed=data['iduser'])
        userrrr = User.objects.filter(id=data['iduser']).first()
        dataToPost = list()
        
        if user_info is not None:
            for user_following in following:
                user = User.objects.filter(id=user_following.id_user_folloing.id).first()
                user_info_following = UserInfo.objects.filter(id_user=user.id).first()

                following = Follow.objects.filter(id_user_folloing=user.id)
                your_followers = Follow.objects.filter(id_user_followed=user.id)
                
                follow =  Follow.objects.filter(id_user_folloing=user_info.id_user.id, id_user_followed=user.id)
                followQuestion = 0

                if len(follow) is not 0:
                    followQuestion = 1
                if user_info.id_user.id is user.id:
                    followQuestion = 2

                datatoapend = {
                    "mainname": userrrr.username,
                    "id": user.id,
                    "username": user.username,
                    "is_superuser": user.is_superuser,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "img": user_info_following.img,
                    "desc": user_info_following.desc,
                    "following": str(len(following)),
                    "your_followers": str(len(your_followers)),
                    "followQuestion": followQuestion,
                }
                dataToPost.append(datatoapend)

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)



















class getuserbyid(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(id_user=data['iduser']).first()

        if user_info is not None:
            user = User.objects.filter(id=user_info.id_user.id).first()
            you_info = UserInfo.objects.filter(token=data['token']).first()

            following = Follow.objects.filter(id_user_folloing=user.id)
            your_followers = Follow.objects.filter(id_user_followed=user.id)
            follow =  Follow.objects.filter(id_user_folloing=you_info.id_user.id, id_user_followed=user.id)
            followQuestion = 0

            if len(follow) is not 0:
                followQuestion = 1
            if you_info.id_user.id is user.id:
                followQuestion = 2

            dataToPost = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "img": user_info.img,
                "desc": user_info.desc,
                "following": str(len(following)),
                "your_followers": str(len(your_followers)),
                "followQuestion": followQuestion,
            }
            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)






class getUsersPosts(View):
    def post(self, request):
        idUser = str(request.body)[2:-1]
        user_info = UserInfo.objects.filter(id_user=int(idUser)).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.filter(writer=int(idUser)).order_by('-publish_date')

            for postTMP in allposts:
                if postTMP.in_response is None:

                    user_followed = User.objects.filter(id = user_info.id_user.id).first()        
                    like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                    likes = Like.objects.filter(id_post = postTMP)    
                    replies = Post.objects.filter(in_response = postTMP.id)

                    if like is not None: 
                        info = { 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                        dataToPost.append(info)
                    else:
                        info = { 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                        dataToPost.append(info)

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)












class post(View):
    def post(self, request):
        data = json.loads(request.body)

        user_info = UserInfo.objects.filter(token=data['token']).first()
        
        if user_info is not None:
            if data['body'] is not None and data['body'] is not '':

                filename = ''
                if 'image' in data and data['image'] is not None:
                    x = data['image'].split(",")
                    imgdata = base64.b64decode(x[1])
                    path = 'final_api/static/public/'
                    filename = str(uuid4()) + '_postpic.png'
                    endfilename = path + '' + filename
                    with open(endfilename, 'wb') as f:
                        f.write(imgdata)


                Post.objects.create(
                    writer = user_info.id_user,
                    body = data['body'], 
                    images = filename, 
                    publish_date = date.today(),
                )

                return JsonResponse(1, safe=False)
        return JsonResponse('no', safe=False)



class postresponse(View):
    def post(self, request):
        data = json.loads(request.body)

        user_info = UserInfo.objects.filter(token=data['token']).first()
        if user_info is not None:
            if data['body'] is not None and data['body'] is not '':

                filename = ''
                if 'image' in data and data['image'] is not None:
                    x = data['image'].split(",")
                    imgdata = base64.b64decode(x[1])
                    path = 'final_api/static/public/'
                    filename = str(uuid4()) + '_postpic.png'
                    endfilename = path + '' + filename
                    with open(endfilename, 'wb') as f:
                        f.write(imgdata)


                Post.objects.create(
                    writer = user_info.id_user,
                    body = data['body'], 
                    images = filename, 
                    publish_date = date.today(),
                    in_response = data['idposttorespond']
                )

                return JsonResponse(1, safe=False)
        return JsonResponse('no', safe=False)









class like(View):
    def post(self, request):
        data =  json.loads(request.body)
        post = Post.objects.filter(id=data['idpost']).first()
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user = User.objects.filter(id=user_info.id_user.id).first()

        if user_info is not None:
            Like.objects.create(
                id_post = post, 
                id_user = user,
            )
            return JsonResponse(data, safe=False)
        return JsonResponse("no", safe=False)



class unlike(View):
    def post(self, request):
        data =  json.loads(request.body)
        post = Post.objects.filter(id=data['idpost']).first()
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user = User.objects.filter(id=user_info.id_user.id).first()

        if user_info is not None:
            Like.objects.filter(id_post=post.id, id_user=user.id).delete()
            return JsonResponse("1", safe=False)
        return JsonResponse("no", safe=False)











class follow(View):
    def post(self, request):
        data =  json.loads(request.body)
        user_follow = User.objects.filter(id=data['iduser']).first()
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user = User.objects.filter(id=user_info.id_user.id).first()

        if user_info is not None:
            Follow.objects.create(
                id_user_followed = user_follow, 
                id_user_folloing = user,
            )
            return JsonResponse(data, safe=False)
        return JsonResponse("no", safe=False)



class unfollow(View):
    def post(self, request):
        data =  json.loads(request.body)
        user_unfollow = User.objects.filter(id=data['iduser']).first()
        user_info = UserInfo.objects.filter(token=data['token']).first()
        user = User.objects.filter(id=user_info.id_user.id).first()

        if user_info is not None:
            Follow.objects.filter(id_user_followed=user_unfollow.id, id_user_folloing=user.id).delete()
            return JsonResponse("1", safe=False)
        return JsonResponse("no", safe=False)












class removepost(View):
    def post(self, request):
        data =  json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:

            responses = Post.objects.filter(in_response=data['idpost'])
            for responseTMP in responses:
                responseTMP.in_response = 0
                responseTMP.save()

            likes = Like.objects.filter(id_post=data['idpost']).delete()
            post = Post.objects.filter(id=data['idpost']).delete()

            return JsonResponse("1", safe=False)
        return JsonResponse("no", safe=False)










class getPost(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:
            post = Post.objects.filter(id=data['idpost']).first()
                        
            user_followed = User.objects.filter(id = post.writer.id).first()
            user_info_followed = UserInfo.objects.filter(id_user=post.writer.id).first()
        
            like = Like.objects.filter(id_user = user_info.id_user, id_post = post).first()    
            likes = Like.objects.filter(id_post = post)    
            replies = Post.objects.filter(in_response = post.id)

            if like is not None: 
                info = { 'inreplies': post.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': post.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_info_followed.img, 'postImage': post.images, 'text': post.body, 'like': 1}   
                return JsonResponse(info, safe=False)

            else:
                info = { 'inreplies': post.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': post.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_info_followed.img, 'postImage': post.images, 'text': post.body, 'like': 0}   
                return JsonResponse(info, safe=False)

        return JsonResponse('no', safe=False)






class getResponsePosts(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:
            dataToPost = list()
            allposts = Post.objects.filter(in_response=data['idpost']).order_by('-publish_date')
            allfollows = User.objects.all()
                
            for postTMP in allposts:
                if postTMP.in_response is not None:
                    for followTMP in allfollows:
                        if postTMP.writer.id == followTMP.id:

                            user_followed = User.objects.filter(id = followTMP.id).first()        
                            user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                            like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                            likes = Like.objects.filter(id_post = postTMP)
                            replies = Post.objects.filter(in_response = postTMP.id)

                            if like is not None: 
                                info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                dataToPost.append(info)
                            else:
                                info = { 'inreplies': postTMP.in_response, 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                dataToPost.append(info)

                            break

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)














































