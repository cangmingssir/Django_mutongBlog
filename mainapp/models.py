from django.db import models
from tinymce.models import HTMLField



class Author(models.Model):
    username=models.CharField(max_length=20,unique=True)
    passwd=models.CharField(max_length=12)
    phone = models.CharField(max_length=11)
    token = models.CharField(max_length=32,null=True)
    photo = models.ImageField(upload_to='userphotos')
    email = models.CharField(max_length=20)

    def toDict(self):
        return {'username':self.username,
                'passwd':self.passwd,
                'phone':self.phone,
                'token':self.token,
                'photo':self.photo.name,
                'email':self.email}


class Blog(models.Model):
    title=models.CharField(max_length=50)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    pubTime = models.DateTimeField(auto_now_add=True)
    content = HTMLField(default='')
    scanCnt = models.IntegerField(default=0)



class Revert(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    content=HTMLField(default='')
