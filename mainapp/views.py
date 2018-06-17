import hashlib
import os
import random
import uuid
from io import BytesIO

from django.http import JsonResponse, HttpResponse
from django.urls import reverse

from MuTongBlog import settings
from django.shortcuts import render, redirect
from mainapp.models import *
from PIL import Image,ImageDraw,ImageFont

# Create your views here.

#主页面
def homepage(request):
    token = request.COOKIES.get('token')
    if request.method=='GET' and token==None:
        return render(request,'homepage.html',
                      {'blogs':Blog.objects.all()})
    user=Author.objects.filter(token=token).last().toDict()
    # blogs = Blog.objects.filter(author_id=user.id)

    return render(request,'homepage.html',
           {'blogs':Blog.objects.all(),
            'data':user})

#登录界面
def userLogin(request):
    token = request.COOKIES.get('token')
    if token:
        return HttpResponse("<script>"
                            "if (confirm('已登录，是否返回主页面'){"
                            "window.location.href='/blog/home/'})"
                            "</script>")
    if request.method=='GET':
        return render(request,'userLogin.html')

    #通过POST请求获取用户输入验证码数据于生成的验证码做比对
    inputVerifyCode = request.POST.get('verifycode')
    sessionVerifyCode=request.session.get('verifycode')
    if inputVerifyCode!=sessionVerifyCode:
        return render(request,'userLogin.html',
                      {'error_msg':'验证码输入错误'})
    user=Author.objects.filter(username=request.POST.get('username'),
                               passwd=request.POST.get('passwd'))
    if user.exists():
        print('用户',user)
        #将用户信息存入session中
        request.session['user'] = user.last().toDict()
        #将验证过的验证码从session中删除
        del request.session['verifycode']
        loginUser = user.last()
        request.session['loginUserId'] = loginUser.id
        resp=redirect('/blog/home/')
        #生成token并保存至数据库
        md5 = hashlib.md5()
        md5.update(str(uuid.uuid4()).encode())
        loginUser.token = md5.hexdigest()
        print('token',loginUser.token)
        loginUser.save()
        #将user信息存入到cookie中
        resp.set_cookie('token',loginUser.token)
        return resp
    else:
        return render(request,'userLogin.html',
                      {'usererror':'您输入的用户名或密码不存在'})




#注册界面
def userSign(request):
    if request.method=='GET':
        return render(request,'userSign.html')



#上传头像
def upload(request):
    # print('图片')
    if request.method=='POST':
        uploadFile = request.FILES.get('img')   #得到上传图片的对象
        saveFileName = str(uuid.uuid4())+'.jpg'
        #settings需要导包，当前项目下的settings
        saveFilePath = os.path.join(settings.MEDIA_ROOT,saveFileName)

        with open(saveFilePath,'wb') as f:
            for part in uploadFile.chunks():
                f.write(part)
                f.flush()
    return JsonResponse({'imgName':saveFileName})


#添加用户信息，保存至数据库
def addUser(request):
    parmer=request.GET if request.method=='GET' else request.POST
    user = Author()
    user.username=parmer.get('username')
    user.passwd=parmer.get('userpasswd')
    user.phone=parmer.get('userphone')
    user.email=parmer.get('useremail')
    user.photo=parmer.get('imageName')
    user.save()
    return redirect('/blog/userLogin/')


#生成验证码
def verifycode(request):
    print('你好')
    #创建画布对象
    img = Image.new(mode='RGB',size=(120,30),color=(220,220,180))

    #创建画笔
    drow = ImageDraw.Draw(img,'RGB')

    #选取字符的范围集合
    chars=''
    while len(chars)<4:
        flog = random.randrange(3)
        charNum = chr(random.randint(48,57)) if not flog else\
                chr(random.randint(65,90)) if flog==1 else\
                chr(random.randint(97,122))
        #排除重复
        if len(chars)==0 or chars.find(charNum):
            chars +=charNum
    #将生成的验证码存入到session中，防止服务端获取到验证码
    request.session['verifycode']=chars
    font = ImageFont.truetype(font='static/fonts/hktt.ttf',size=25)

    #随机产生4位验证码
    for char in chars:
        color = (random.randrange(255),
                 random.randrange(255),
                 random.randrange(255),)
        #设置每个验证码的位置，纵向位置和高
        xy=(15 + chars.find(char) * 20 ,random.randrange(2,8))
        drow.text(xy=xy,
                  text=char,
                  fill=color,
                  font=font)

    #验证码背景，200个不同颜色的点
    for i in range(200):
        xy =(random.randrange(120),random.randrange(30))
        color = (random.randrange(255),
                 random.randrange(255),
                 random.randrange(255),)
        drow.point(xy=xy,fill=color)

    #将画布对象转成二进制数据
    buffer = BytesIO()  #创建字节缓存对象
    img.save(buffer,'png')  #指定图片格式，并将img对象存入缓冲中
    print("image",buffer.getvalue())
    #清理队形的引用
    del drow
    del img
    return HttpResponse(buffer.getvalue(),
                    content_type='image/png')

#点击博客标题查看具体信息
def show(request,blog_id):
    print("ID:",blog_id)
    print()
    blog=Blog.objects.get(id=blog_id)
    return render(request,'showBlog.html',
                  {"blog":blog})

#退出登录
def logout(request):
    resp=redirect('/blog/home/')
    resp.delete_cookie('token')
    request.session.clear()
    return resp

#发布博客
def wirteBlog(request):
    if request.method=='GET':
        return render(request,'wirteBlog.html',
                      {'author_id':Author.objects.get(username=request.GET.get('user_name')).id})
    blog = Blog()
    blog.title=request.POST.get('title')
    print("标题",blog.title)
    blog.content=request.POST.get('content')
    print("内容",blog.content)
    blog.author_id=request.POST.get('author_id')
    blog.save()

    return redirect('/blog/home/')

#保存评论
def revert(request):
    user = Author.objects.filter(token=request.COOKIES.get('token'))
    revert = Revert()
    revert.author_id=user.last().id
    revert.blog_id=request.POST.get('blog_id')
    revert.content=request.POST.get('revertCotent')
    revert.save()
    return redirect(reverse('show',args=(revert.blog_id,)))