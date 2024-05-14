app_name='security'
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import ProfileUpdateView

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/security/login'),name='logout'),
    path('edit/',ProfileUpdateView.as_view(),name='profile_edit'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)