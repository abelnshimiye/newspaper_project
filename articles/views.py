

from dataclasses import fields
from pyexpat import model
from urllib import request
from django.shortcuts import render


# authorizitions with Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# permission to allow the othor to edit, delete or update its article
from django.core.exceptions import PermissionDenied

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article

from django.urls import reverse_lazy

# Create your views here.

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    login_url = 'login' # add this to tell our app that we are on user/login not account/login

class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login' # add this to tell our app that we are on user/login not account/login

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login' # add this to tell our app that we are on user/login not account/login

    # function to check the othor
    def dispatch(self, request, *args, **kwargs) :
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login' # add this to tell our app that we are on user/login not account/login

    def dispatch(self, request, *args, **kwargs) :
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body',)
    login_url = 'login' # add this to tell our app that we are on user/login not account/login

    # add othor automatically from 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)