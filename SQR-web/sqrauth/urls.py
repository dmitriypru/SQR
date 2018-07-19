from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.authentication, name="authentication"),
    url(r'^logout/$', views.log_out, name="log_out"),
]