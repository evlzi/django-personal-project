from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', AccountPage.as_view(), name = 'account_list'),
    path('signup/', SignUpPage.as_view(), name = 'account_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='account/account_login.html'), name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='account_logout'),
]
