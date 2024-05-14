# security/forms.py
from django import forms
from django.contrib.auth import get_user_model

# カスタムユーザーモデルを取得
User = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'avatar']
        labels={
            'first_name':'ユーザーネーム',
            'avatar':'プロフィール画像',
        }
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'avatar':forms.FileInput(attrs={'class':'form-control-file'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'avatar')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'avatar')
