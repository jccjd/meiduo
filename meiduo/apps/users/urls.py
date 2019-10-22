from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'users'
urlpatterns = [
    url(r'register/', views.RegisterView.as_view(), name='register'),

    url(r'change/', views.ChangePasswdView.as_view(), name='pass'),

    url(r'login/', views.LoginView.as_view(), name='login'),

    url(r'logout/', views.LogoutView.as_view(), name='logout'),

    url(r'info/', login_required(views.UserInfoView.as_view()), name='info'),

    url(r'^emails/$', views.EmailView.as_view(), name='email'),

    url(r'^emails/verification/$', views.VerifyEmailView.as_view(), name='verify_email'),

    url(r'^addresses/$', views.AddressView.as_view(), name='address'),

    url(r'^addresses/create/$', views.AddressCreateView.as_view()),

    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),

    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),

    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),


    url(r'browse_histories/', views.UserBrowseHistory.as_view()),
]
