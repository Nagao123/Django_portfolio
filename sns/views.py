from django.shortcuts import render,redirect
from .models import Message,Good
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required(login_url='/security/login/')
def index(request):
    message=Message.objects.all()
    error=''
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            # commit=Falseはsaveを保留する
            message2=form.save(commit=False)
            message2.owner=request.user
            message2.save()
            return redirect('sns:index')
        else:
            error='投稿に失敗しました。'
            return redirect('sns:index')
    else:
        form=MessageForm()
    params={
        'login_user':request.user,
        'message':message,
        'form':form,
        'error':error,
    }
    return render(request,'sns/index.html',params)

@login_required(login_url='/security/login')
def good(request,good_id):
    good_msg=Message.objects.get(id=good_id)
    is_good=Good.objects.filter(owner=request.user).filter(message=good_msg).count()
    is_good_instance=Good.objects.filter(owner=request.user).filter(message=good_msg)
    if is_good==1:
        is_good_instance.delete()
        good_msg.good_count-=1
        good_msg.save()
        return redirect('sns:index')
    else:
        good_msg.good_count+=1
        good_msg.save()
        good=Good()
        good.owner=request.user
        good.message=good_msg
        good.save()
        messages.success(request,'goodをしました')
        return redirect('sns:index')

@login_required(login_url='/security/login')
def goods_view(request):
    goods=Good.objects.filter(owner=request.user)
    params={
        'goods':goods,
        'login_user':request.user,
    }
    return render(request,'sns/goods.html',params)

@login_required(login_url='/security/login/')
def good_remove(request,good_id):
    good=Good.objects.get(id=good_id)
    good.delete()
    good.message.good_count-=1
    good.message.save()
    return redirect('sns:goods_view')


from security.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import Follow

@login_required(login_url='security/login/')
def my_account(request):
    message=Message.objects.filter(owner=request.user)
    params={
        'message':message,
        'login_user':request.user,
    }
    return render(request,'sns/my_account.html',params)

@login_required(login_url='security/login/')
def tweet(request):
    if request.method=='POST':
        form=MessageForm(request.POST,request.FILES)
        if form.is_valid():
            message=form.save(commit=False)
            message.owner=request.user
            message.save()
            return redirect('sns:index')
        else:
            return redirect('sns:tweet')
    else:
        form=MessageForm()
    params={
        'login_user':request.user,
        'form':form,
    }
    return render(request,'sns/tweet.html',params)

from .forms import CommentForm
from .models import Comment

@login_required(login_url='security/login/')
def comment_view(request,msg_id):
    message=get_object_or_404(Message,id=msg_id)
    comments=Comment.objects.filter(message=message)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.owner=request.user
            comment.message=message
            comment.save()
            params={
                'form':form,
                'm':message,
                'comments':comments,
                'login_user':request.user,
            }
            return redirect('sns:comment',msg_id=msg_id)
    else:
        form=CommentForm()
    params={
        'form':form,
        'm':message,
        'comments':comments,
        'login_user':request.user
    }
    return render(request,'sns/comment.html',params)

from .models import Comment_Good

@login_required(login_url='security/login')
def comment_good(request,comment_id):
    # いいねをしたコメントの抽出
    comment=get_object_or_404(Comment,id=comment_id)
    is_good=Comment_Good.objects.filter(owner=request.user).filter(comment=comment)
    is_good_count=is_good.count()
    if is_good_count==1:
        is_good.delete()
        comment.good_count-=1
        comment.save()
        return redirect ('sns:comment',msg_id=comment.message.id)
    else: 
        comment.good_count+=1
        comment.save()
        is_comment_good=Comment_Good()
        is_comment_good.owner=request.user
        is_comment_good.comment=comment
        is_comment_good.save()
        return redirect ('sns:comment',msg_id=comment.message.id)

@login_required(login_url='security/login')
def user_post_list(request,user_id):
    user=get_object_or_404(CustomUser,id=user_id)
    message=Message.objects.filter(owner=user)
    params={
        'message':message,
        'login_user':request.user,
    }
    return render(request,'sns/user_post_list.html',params)

def delete_post(request,msg_id):
    msg=get_object_or_404(Message,id=msg_id)
    if request.method=='POST' and msg.owner==request.user:
        msg.delete()
        return redirect('sns:my_account')
    else:
        return redirect('sns:index')