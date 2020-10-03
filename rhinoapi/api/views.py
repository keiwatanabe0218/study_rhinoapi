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
from .models import Object, MoveObjects, TwistedTower
from .serializers import ObjectSerializer, UserSerializer, MoveObjectsSerializer, TwistedTowerSerializer
from .ownpermissions import ProfilePermission
from .rhino_commands.commands import create_box, move_objects, twisted_tower_command

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
    
    # rhinoのurllib2がdata付きでGETたたけないのでPOSTで代用
    @action(methods=["post"], detail=False)
    def get(self, request):
        print(request)
        user = request.user
        title = request.data['title']


        vm = MoveObjects.objects.filter(title = title, created_by = user)[0]

        serializer = MoveObjectsSerializer(vm)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TwistedTowerViewSet(viewsets.ModelViewSet):
    # モデル
    queryset = TwistedTower.objects.all()
    # シリアライザー
    serializer_class = TwistedTowerSerializer
    # ユーザー認証
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Twisted TowerをつくるAPI
    @action(methods=["post"], detail=False)
    def create_twisted_tower(self, request):
        # リクエストからパラメータを取得
        user = request.user
        title = request.data['title']
        base_curve = request.data['base_curve']
        center_point = request.data['center_point']
        angle = request.data['angle']
        height = request.data['height']
        twisted_tower = twisted_tower_command(base_curve, center_point, float(angle), float(height))

        # 以前のモデルのデータを削除する
        pre_vm = TwistedTower.objects.all()
        pre_vm.delete()
        # モデルを作成
        item = TwistedTower(title=title, base_curve=base_curve, center_point=center_point, twisted_tower=twisted_tower, angle=angle, height=height,created_by=user)
        item.save()

        # シリアライズ
        serializer = TwistedTowerSerializer(data={"title": title, "base_curve":base_curve, "center_point":center_point, "twisted_tower":twisted_tower,
                                                    'angle':angle, 'height':height}, context={'request': request})
        
        # シリアライザが有効なら200、無効なら400を返す
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DBにあるモデルを参照するAPI
    # rhinoのurllib2がdata付きでGETたたけないのでPOSTで代用
    @action(methods=["post"], detail=False)
    def get(self, request):
        user = request.user
        title = request.data['title']

        # リクエストから取得したタイトルのモデルを取得
        vm = TwistedTower.objects.filter(title = title, created_by = user)[0]
        # シリアライズ
        serializer = TwistedTowerSerializer(vm)
        # データを返す
        return Response(serializer.data, status=status.HTTP_200_OK)