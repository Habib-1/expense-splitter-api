from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
User=get_user_model()
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]