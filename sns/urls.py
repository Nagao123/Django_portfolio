app_name='sns'
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('good/<int:good_id>',views.good,name='good'),
    path('goods_view/',views.goods_view,name='goods_view'),
    path('good_remove/<int:good_id>',views.good_remove,name='good_remove'),
    path('my_account/',views.my_account,name='my_account'),
    path('tweet/',views.tweet,name='tweet'),
    path('comment/<int:msg_id>',views.comment_view,name='comment'),
    path('comment_good/<int:comment_id>',views.comment_good,name='comment_good'),
    path('post_list/<int:user_id>',views.user_post_list,name='user_post_list'),
    path('post_delete/<int:msg_id>',views.delete_post,name='post_delete'),
]