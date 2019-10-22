from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'areas'
urlpatterns = [
    url(r'areas/', views.AreasView.as_view(), name='areas'),
]
