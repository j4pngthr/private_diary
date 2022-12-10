from django.shortcuts import render

import logging

from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Diary

# Create your views here.
logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました．')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# 日記一覧ページを表示
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'
    # ページネーションをつける
    paginate_by = 2

    def get_queryset(self):
        # ログインしているユーザーのインスタンスを取得
        # 作成日時で降順に
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries