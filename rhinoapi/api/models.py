from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Object(models.Model):
    title = models.CharField(max_length=50)
    objs = models.CharField(blank=True, max_length=1000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class MoveObjects(models.Model):
    title = models.CharField(max_length=50)
    objs = models.CharField(blank=True, max_length=10000000)
    moved_objs = models.CharField(blank=True, max_length=10000000)
    mov_x = models.CharField(max_length=50)
    mov_y = models.CharField(max_length=50)
    mov_z = models.CharField(max_length=50)
    mov_count = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TwistedTower(models.Model):
    # タイトル
    title = models.CharField(max_length=50)
    # ベースカーブ
    base_curve = models.TextField(blank=True)
    # 中心点
    center_point = models.TextField(blank=True)
    # タワー
    twisted_tower = models.TextField(blank=True)
    # ねじれ角度
    angle = models.CharField(max_length=50)
    # タワーの高さ
    height = models.CharField(max_length=50)   
    # 作成日
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日
    updated_at = models.DateTimeField(auto_now=True)
    # 作成者
    created_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title