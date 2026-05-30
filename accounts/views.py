from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView

from cart.views import merge_guest_cart_to_user
from .forms import CustomSignupForm, LoginForm, ProfileForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('accounts:login')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        merge_guest_cart_to_user(self.request, self.request.user)
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


@method_decorator(login_required, name='dispatch')
class UpdateProfileView(View):
    template_name = 'accounts/profile_update.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
