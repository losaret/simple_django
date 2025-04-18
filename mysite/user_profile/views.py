from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from.forms import RegistrationForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
# Create your views here.
'''
class RegistrationView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = "registration/registration.html"
'''
@csrf_protect
@require_http_methods(["POST", "GET"])
def registration_view(request):
    if request.method == "GET":
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'registration/registration.html', {'form': form})