# Create your models here.
from django.db import models
from django.conf import settings
# Create your models here.

class Follow(models.Model):
    follower=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='following',on_delete=models.CASCADE)
    followed=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='followers',on_delete=models.CASCADE)
    pub_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('follower','followed')
    
    def __str__(self):
        return f'{self.follower} follow {self.followed}'

class Message(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='message_owner')
    content=models.TextField(max_length=1000)
    photo=models.ImageField(upload_to='photo/',null=True,blank=True)
    good_count=models.IntegerField(default=0)
    pub_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.content} by {self.owner}'
    
    class Meta:
        ordering=('-pub_date',)

class Good(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='good_owner')
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    pub_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.message} by{self.owner}'
    
    class Meta:
        ordering=('-pub_date',)

class Comment(models.Model):
    message=models.ForeignKey(Message,on_delete=models.CASCADE,related_name='comments')
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='comment',on_delete=models.CASCADE)
    content=models.TextField(max_length=1000)
    pub_date=models.DateTimeField(auto_now_add=True)
    good_count=models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.message} commented by {self.owner}'
    
    class Meta:
        ordering=['-good_count','pub_date',]

class Comment_Good(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_good_owner')
    pub_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.message} by {self.owner}'