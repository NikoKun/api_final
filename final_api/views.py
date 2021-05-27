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

# django-cors-headers


class test(View):
    def get(self, request):

        data = [{ 'name': 'NikoKun', 'image': 'img1.jpg', 'verified': True, 'text': 'Increible Tweet'}, 
                { 'name': 'Timuru', 'image': 'img2.jpg', 'verified': True, 'text': 'I love Juicy Asians'}, 
                { 'name': 'Timuru', 'image': 'img2.jpg', 'verified': True, 'text': 'I love Juicy Asians'},
                { 'name': 'Timuru', 'image': 'img2.jpg', 'verified': True, 'text': 'I love Juicy Asians'},
                { 'name': 'Carlos', 'image': 'img3.jpg', 'verified': True, 'text': 'De locos...'}]

        return JsonResponse(data, safe=False)



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
        response = [{ 'response': 0, 'token': 'no'}]

        if user is not None:
            user_info = UserInfo.objects.filter(id_user=user.id).first()
            response = [{ 'response': 1, 'token': user_info.token}]
            return JsonResponse(response, safe=False)
        return JsonResponse('Username or password is incorrect.', safe=False)






class getuser(View):
    def post(self, request):
        tokenVar = str(request.body)[2:-1]
        user_info = UserInfo.objects.filter(token=tokenVar).first()

        if user_info is not None:
            user = User.objects.filter(id=user_info.id_user.id).first()
            dataToPost = {
                "username": user.username,
                "is_superuser": user.is_superuser,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "img": user_info.img,
                "desc": user_info.desc,
            }
            return JsonResponse(dataToPost, safe=False)
        return "no"







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








