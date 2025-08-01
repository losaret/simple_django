from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm, ExtendUserForm, UserForm
from .models import ExtendUser
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from allauth.account.utils import send_email_confirmation
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
            send_email_confirmation(request, user)
            login(request, user)
            return redirect('home')
    return render(request, 'registration/registration.html', {'form': form})
    
class UpdateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'vkusno/update_profile.html'
    success_url = reverse_lazy('user_profile:profile')

    def get_object(self):
        return self.request.user
    
    def get_form_class(self):
        # Возвращаем основную форму (UserForm)
        return UserForm
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserForm(instance=self.request.user)
        if 'extend_form' not in context:
            context['extend_form'] = ExtendUserForm(instance=self.request.user.extenduser)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserForm(request.POST, instance=request.user)
        extend_form = ExtendUserForm(request.POST, request.FILES, instance=request.user.extenduser)
        
        if user_form.is_valid() and extend_form.is_valid():
            user_form.save()
            extend_form.save()
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form, extend_form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, user_form, extend_form):
        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                extend_form=extend_form
            )
        )