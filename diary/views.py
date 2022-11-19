from django.shortcuts import render

# Create your views here.
from django.views import generic
from .forms import InquiryForm

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm