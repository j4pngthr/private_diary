from django.shortcuts import render

import logging

from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm, DiaryCreateForm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Diary
# from .models import Post

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

class DetailView(generic.DetailView):
    model = Post
    slug_field = "title" # モデルのフィールド名
    slug_url_kwarg = "title" # urls.pyでのキーワードの名前

class DiaryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Diary
    template_name = 'diary_detail.html'
    pk_url_kwarg = 'id'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    # 正常に処理が完了したら，日記一覧ページに遷移
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました．')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました．")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました．')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, '日記の更新に失敗しました．')
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました．")
        return super().delete(request, *args, **kwargs)