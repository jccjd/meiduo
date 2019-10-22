from django.conf.urls import url

from meiduo.apps.contents import views
app_name = 'contents'
urlpatterns = [
    url(r'', views.IndexView.as_view(), name='index'),
]
