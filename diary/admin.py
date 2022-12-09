from django.contrib import admin

from .models import Diary
# Register your models here.
# 日記テーブルを管理サイトで編集
admin.site.register(Diary)