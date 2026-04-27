from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.views.generic import UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm, ExtendUserForm, UserForm
from .models import ExtendUser
from allauth.account.utils import send_email_confirmation



'''
class RegistrationView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = "registration/registration.html"

'''

User = get_user_model()

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
            #send_email_confirmation(request, user)
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

class FollowView(View):
    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username).extenduser
        current_user = request.user.extenduser
        if current_user == user_to_follow:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Нельзя подписаться на себя'
                }, status=400)
            return redirect('home')

        is_following = current_user.is_following(user_to_follow)

        if is_following:
            current_user.unfollow(user_to_follow)
            action = 'unfollowed'
        else:
            current_user.follow(user_to_follow)
            action = 'followed'
        
        context = {
            'is_following': not is_following,
            'followers_count': user_to_follow.followers_count,
            'action': action,
            'username': username,
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(context)
        
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        return redirect(next_url or 'home', username=username)
    