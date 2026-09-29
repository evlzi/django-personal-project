from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from pages.models import UserProfile

# Create your views here.


class SignUpPage(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/account_signup.html'


class AccountPage(ListView):
    model = UserProfile
    template_name = 'account/account_list.html'
