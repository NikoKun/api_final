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
                if postTMP.in_response is None:
                    for followTMP in allfollows:
                        if postTMP.writer.id == followTMP.id_user_followed.id or postTMP.writer.id == user_info.id_user.id:

                            user_followed = User.objects.filter(id = followTMP.id).first()        
                            user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                            like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                            likes = Like.objects.filter(id_post = postTMP)

                            if like is not None: 
                                info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                dataToPost.append(info)
                            else:
                                info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                dataToPost.append(info)

                            break

                    if postTMP.writer.id == user_info.id_user.id:

                        user_followed = User.objects.filter(id = user_info.id_user.id).first()        
                        user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                        like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                        likes = Like.objects.filter(id_post = postTMP)

                        if like is not None: 
                            info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                            dataToPost.append(info)
                        else:
                            info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+' '+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
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
                if postTMP.in_response is None:
                    for followTMP in allfollows:
                        if postTMP.writer.id == followTMP.id:

                            user_followed = User.objects.filter(id = followTMP.id).first()        
                            user_followed_info = UserInfo.objects.filter(id_user=user_followed).first()
                            like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                            likes = Like.objects.filter(id_post = postTMP)
                            replies = Post.objects.filter(in_response = postTMP.id)

                            if like is not None: 
                                info = { 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                                dataToPost.append(info)
                            else:
                                info = { 'replies': len(replies), 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_followed_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                                dataToPost.append(info)

                            break


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
                    
                    if like is not None: 
                        info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                        dataToPost.append(info)
                    else:
                        info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                        dataToPost.append(info)

            return JsonResponse(dataToPost, safe=False)
        return JsonResponse('no', safe=False)












class post(View):
    def post(self, request):
        data = json.loads(request.body)

        user_info = UserInfo.objects.filter(token=data['token']).first()

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
        return JsonResponse('Need to write something...', safe=False)





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


class removepost(View):
    def post(self, request):
        data =  json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:

            responses = Post.objects.filter(in_response=data['idpost'])
            for responseTMP in responses:
                responseTMP.in_response = 0
                responseTMP.save()
            post = Post.objects.filter(id=data['idpost']).delete()

            return JsonResponse("1", safe=False)
        return JsonResponse("no", safe=False)










class getPost(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:
            post = Post.objects.filter(id=data['idpost']).first()
                        
            if post.in_response is None:

                user_followed = User.objects.filter(id = post.writer.id).first()
                user_info_followed = UserInfo.objects.filter(id_user=post.writer.id).first()
        
                like = Like.objects.filter(id_user = user_info.id_user, id_post = post).first()    
                likes = Like.objects.filter(id_post = post)    
                
                if like is not None: 
                    info = { 'likes': len(likes), 'idpost': post.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info_followed.img, 'postImage': post.images, 'text': post.body, 'like': 1}   
                    return JsonResponse(info, safe=False)

                else:
                    info = { 'likes': len(likes), 'idpost': post.id, 'iduser': user_followed.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info_followed.img, 'postImage': post.images, 'text': post.body, 'like': 0}   
                    return JsonResponse(info, safe=False)

            return JsonResponse('no', safe=False)
        return JsonResponse('no', safe=False)





class getResponsePosts(View):
    def post(self, request):
        data = json.loads(request.body)
        user_info = UserInfo.objects.filter(token=data['token']).first()

        if user_info is not None:
            post = Post.objects.filter(id=data['idpost']).first()
            responses = Post.objects.filter(in_response=data['idpost']).first()
            dataToPost = list()

            if responses is not None:
                for postTMP in responses:
                    if post.in_response is None and postTMP.in_response is not None:

                        user_followed = User.objects.filter(id = postTMP.writer.id).first()   
                        user_info_followed = UserInfo.objects.filter(id_user=postTMP.writer.id).first()     
                        like = Like.objects.filter(id_user = user_info.id_user, id_post = postTMP).first()    
                        likes = Like.objects.filter(id_post = postTMP)    

                        if like is not None: 
                            info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'responseTo': post.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info_followed.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 1}   
                            dataToPost.append(info)
                        else:
                            info = { 'likes': len(likes), 'idpost': postTMP.id, 'iduser': user_followed.id, 'responseTo': post.id, 'name': user_followed.username, 'lastnames': user_followed.first_name+''+user_followed.last_name, 'image': user_info_followed.img, 'postImage': postTMP.images, 'text': postTMP.body, 'like': 0}   
                            dataToPost.append(info)
                return JsonResponse(dataToPost, safe=False)
            return JsonResponse('no', safe=False)
        return JsonResponse('no', safe=False)



""" -------------------------------------------------------------------------------------------------------------------------------- """


""" 






class getHomePosts(View):
    def post(self, request):
        user_info = UserInfo.objects.filter(token=request.POST['token']).first()

        if user_info is not None:
            allposts = Post.objects.all().order_by('-date')
            allfollows = Follow.objects.filter(id_user_followed = user.id)

            followedposts = {}
            followedperson = {}

            for postTMP in allposts:
                for followTMP in allfollows:
                    if postTMP.writer == followTMP.id_user_followed:
                        followedposts[postTMP.id] = postTMP
                        followedperson[followTMP.id] = followTMP
                        break

            dataToPost = {
                "name": User.objects.filter(id=user_info.id_user).first(),
                "user_info": user_info,
                "posts": followedposts,
                "following": followedperson
            }
            return dataToPost
        return "no"

 """








