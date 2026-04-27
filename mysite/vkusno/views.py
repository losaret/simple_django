import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import View, DeleteView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import product_card, categories
from .forms import PublishCardForm, PublishCategoryForm
from user_profile.models import ExtendUser
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

# Create your views here.

logger = logging.getLogger("django")

class Index(LoginRequiredMixin, View):
    """ Index page reachable from / URL"""
    def get(self, request):
        params = dict()
        userprofile = User.objects.filter(username=request.user.username).first()
        query = Q(user=userprofile)
        search_query = ''
        cards = product_card.objects.filter(query)
        categories_view = categories.objects.filter(query)
        params['cards'] = cards
        params['search_query'] = search_query
        params['profile'] = userprofile
        params['card_form'] = PublishCardForm()
        params['category_form'] = PublishCategoryForm()
        params['categories'] = categories_view
        return render(request, 'vkusno/self_profile.html', params)
    
class PublishCard(LoginRequiredMixin, View):
    def post(self, request):
        form = PublishCardForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = User.objects.get(username=request.user.username)
            image = request.FILES['card_image']
            text = form.cleaned_data['comment']
            category_name = request.POST.get('category')
            try:
                card_category = categories.objects.get(user=userprofile, name=category_name)
            except:
                return HttpResponseRedirect('/')
            card_choice = form.cleaned_data['choice']
            published_card = product_card(
                comment = text,
                user = userprofile,
                card_image = image,
                category = card_category,
                choice = card_choice
            )
            published_card.save()
        return HttpResponseRedirect('/')

class DeleteCard(LoginRequiredMixin, DeleteView):
    model = product_card
    template_name = 'vkusno/card_delete.html'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        # Обеспечиваем, что пользователь может удалять только свои карточки
        return super().get_queryset().filter(user=self.request.user)
            

class PublishCategory(LoginRequiredMixin, View):
    def post(self, request):
        form = PublishCategoryForm(request.POST)
        if form.is_valid():
            userprofile = User.objects.get(username=request.user.username)
            category_name = form.cleaned_data['name']
            published_category = categories(
                user = userprofile,
                name = category_name
            )
            if categories.objects.filter(user=userprofile, name=category_name).exists():
                return HttpResponseRedirect('/')
            else:
                published_category.save()
                logger.info(
                    "SAVE category id=%s name=%s",
                    userprofile.pk,
                    category_name
                )
        return HttpResponseRedirect('/')
    
class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = categories
    form_class = PublishCategoryForm
    template_name = 'vkusno/self_profile.html'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context
    
class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = categories
    template_name = 'vkusno/category_delete.html'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        # Обеспечиваем, что пользователь может удалять только свои категории
        return super().get_queryset().filter(user=self.request.user)
    
class Search(LoginRequiredMixin, View):
    """ Searching cards reachable from from /search/?q=<query> URL """
    def get(self, request):
        search_query = request.GET.get('query')
        params = dict()
        userprofile = User.objects.get(username=request.user.username)
        try:
            cards = product_card.objects.filter(user=userprofile, comment__icontains=search_query)
            params['cards'] = cards
            params['search_query'] = search_query
        except ValueError:
            pass
        return render(request, 'vkusno/search.html', params)

class About(View):
    def get(self, request):
        params = dict()
        userprofile = User.objects.filter(username=request.user.username).first()
        search_query = ''
        params['search_query'] = search_query
        params['profile'] = userprofile
        return render(request, 'vkusno/about.html', params)        

class OtherProfile(View):
    """ View other profile reachable from from /<str:username>/ URL """
    def get(self, request, username):
        params = dict()
        if request.user.username == username:
            return redirect('home')
        try:
            userprofile = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, '404.html', params)  
        query = Q(user=userprofile)
        cards = product_card.objects.filter(query)
        categories_view = categories.objects.filter(query)
        is_following = request.user.extenduser.is_following(userprofile.extenduser)
        params['is_following'] = is_following
        params['cards'] = cards
        params['profile'] = userprofile.extenduser
        params['categories'] = categories_view
        return render(request, 'vkusno/other_profile.html', params)