from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^carts/$', views.CartsView.as_view(), name='carts'),

    url(r'^carts/selection/$', views.CartsSelectionView.as_view()),

    url(r'^carts/simple/$', views.CastsSimpleView.as_view())
]
