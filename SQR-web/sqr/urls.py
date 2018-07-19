from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.authtoken import views
from rest_framework import routers
from qruser import views as v
from qruser.views import UserRegisterViewSet, ActionViewSet
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register(r'users', v.UserViewSet, "123")


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/stand/register/', UserRegisterViewSet.as_view()),
    url(r'^api/stand/action/', ActionViewSet.as_view()),
    url(r'^api/stand/auth/', views.obtain_auth_token),
    url(r'^', include('qruser.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('sqrauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
