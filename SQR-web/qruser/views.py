from django.shortcuts import render, HttpResponse, redirect, render_to_response
from .models import User, UserAction
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from django.views.decorators.csrf import ensure_csrf_cookie

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.all().filter(username=user.username)

def index(request):
    if not request.user.is_authenticated():
        return redirect('authentication')
    else:
        secret_word = request.user.secret_word
        actions = UserAction.objects.all().order_by('-date_time')

    return render(request, "index/actionlist.html", {'actions': actions, 'secret_word': secret_word})

def get_qr(request):
    qr = None
    secret_word = None
    if request.user.is_authenticated():
        secret_word = request.user.secret_word
        qr = pyotp.TOTP(secret_word, interval=30).now()
    return HttpResponse(qr)

class UserRegisterViewSet(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class ActionViewSet(CreateAPIView):
    serializer_class = ActionSerializer
    permission_classes = (AllowAny,)
