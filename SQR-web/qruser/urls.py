from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^get_qr', views.get_qr, name="get_qr"),
]