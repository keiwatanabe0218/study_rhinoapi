from django.contrib import auth
from django.http import request
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.serializers import Serializer
from .models import Object, MoveObjects
from .serializers import ObjectSerializer, UserSerializer, MoveObjectsSerializer
from .ownpermissions import ProfilePermission
from .rhino_commands.commands import create_box, move_objects

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

class MoveObjectsViewSet(viewsets.ModelViewSet):
    queryset = MoveObjects.objects.all()
    serializer_class = MoveObjectsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=["post"], detail=False)
    def move(self, request):
        user = request.user
        title = request.data['title']
        objs_json = request.data['objects']
        mov_x = request.data['mov_x']
        mov_y = request.data['mov_y']
        mov_z = request.data['mov_z']
        mov_count = request.data['mov_count']
        moved_objs = move_objects(objs_json, mov_x, mov_y, mov_z, mov_count)

        # 以前のモデルのデータを削除する
        pre_vm = MoveObjects.objects.all()
        pre_vm.delete()
        # モデルを作成
        item = MoveObjects(title=title, objs = objs_json, moved_objs = moved_objs, mov_x = mov_x, mov_y = mov_y, mov_z = mov_z, mov_count = mov_count, created_by=user)
        item.save()


        # シリアライズを行う
        serializer = MoveObjectsSerializer(data={"title": title, "moved_objs":moved_objs, 'objs':objs_json, 'mov_x':mov_x, 'mov_y':mov_y, 'mov_z':mov_z, 'mov_count':mov_count}, context={'request': request})
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # rhinoのurllib2がdata付きでGETたたけない！！！
    @action(methods=["post"], detail=False)
    def get(self, request):
        print(request)
        user = request.user
        title = request.data['title']


        vm = MoveObjects.objects.filter(title = title, created_by = user)[0]

        serializer = MoveObjectsSerializer(vm)

        return Response(serializer.data, status=status.HTTP_200_OK)