from django.contrib import auth
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.contrib.auth.models import User
from .models import Object
from .serializers import ObjectSerializer, UserSerializer
from .ownpermissions import ProfilePermission
from .rhino_commands.commands import create_box

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ProfilePermission,)

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=["post"], detail=False)
    def box(self, request):
        user = request.user
        title = request.data['title']
        width = request.data['width']
        depth = request.data['depth']
        height = request.data['height']
        breps = create_box(width, depth, height)

        # 以前のモデルのデータを削除する
        pre_vm = Object.objects.all()
        pre_vm.delete()
        # モデルを作成
        item = Object(title=title, objs=breps, created_by=user)
        item.save()

        # シリアライズを行う
        serializer = ObjectSerializer(data={"title": title, "objs":breps}, context={'request': request})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)