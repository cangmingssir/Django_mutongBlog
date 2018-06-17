# coding:utf-8
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from mainapp.models import *




class MuBlog(MiddlewareMixin):
#
#     def process_request(self,req):
#         address = req.path
#         if address=='/blog/userLogin/':
#             token = req.COOKIES.get('token')
#             if token:
#                 return HttpResponse('<script>'
#                                     'if (confirm("已登录，是否返回主页面"){'
#                                     'window.location.href="/blog/home/"'
#                                     '})'
#                                     '</script>')
#             else:
#中间键
    def process_request(self,request):
        path=request.path
        print(path)
        print("-------",type(path))
        if path.find('/blog/show')==0:
            id = path.split('/')[-1]
            print("showID",id)
            Blog.objects.filter(id=id).update(scanCnt=F('scanCnt')+1)

