from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User=get_user_model()

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('sns:index')
        else:
            return render(request,'security/login.html',{'error':'無効です。'})
    else:
        # GET リクエスト時の処理
        return render(request, 'security/login.html',{'error':''})

def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        user=User.objects.create_user(username=email,email=email,password=password,first_name=first_name)
        user.save()
        return redirect('security:login')
    else:
        return render(request,'security/signup.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import CustomUserForm
from .models import CustomUser

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm  # 修正: formからform_classに変更
    login_url='/security/login/'
    template_name = 'security/profile_edit.html'
    success_url = reverse_lazy('sns:index')  # success_urlが正しく設定されているか確認
    
    def get_object(self, queryset=None):
        # ログイン中のユーザーインスタンスを返す
        return self.request.user
    
    def get_context_data(self, **kwargs):
        # 既存のコンテキストデータを取得する
        context = super().get_context_data(**kwargs)
        # コンテキストに新しい変数を追加する
        context['login_user'] = self.request.user
        return context
