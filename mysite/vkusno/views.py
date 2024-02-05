from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.views.generic import View
from django.db.models import Q
from .models import product_card, categories
from .forms import PublishForm


# Create your views here.


class index(View):
    """ Index page reachable from / URL"""
    def get(self, request):
        params = dict()
        userprofile = User.objects.get(username=request.user.username)
        query = Q(user=userprofile)
        cards = product_card.objects.filter(query)
        categories_view = categories.objects.filter(query)
        params['cards'] = cards
        params['profile'] = userprofile
        params['form'] = PublishForm()
        params['categories'] = categories_view
        return render(request, 'vkusno/self_profile.html', params)
    
    
class Publishcard(View):
    def post(self, request):
        form = PublishForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = User.objects.get(username=request.user.username)
            image = request.FILES['card_image']
            text = form.cleaned_data['comment']
            card_category = form.cleaned_data['category']
            card_choice = form.cleaned_data['choice']
            published_card = product_card(
                comment = text,
                user = userprofile,
                card_image = image,
                category = card_category,
                choice = card_choice
            )
            published_card.save()
        return HttpResponseRedirect('/vkusno/')

def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url" : image_url
        })
    return render(request, "upload.html")