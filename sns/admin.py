from django.contrib import admin
from .views import Message,Good,Comment
# Register your models here.

admin.site.register(Message)
admin.site.register(Good)
admin.site.register(Comment)