from django.db.models import fields
from django.db.models.fields.related_descriptors import create_reverse_many_to_one_manager
from rest_framework import serializers
from .models import Object, MoveObjects, TwistedTower
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only':True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    
class ObjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Object
        fields = ['id', 'title', 'objs', 'created_at', 'updated_at', 'created_by']


class MoveObjectsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MoveObjects
        fields = ['id', 'title', 'objs', 'moved_objs', 'mov_x', 'mov_y', 'mov_z', 'mov_count', 'created_at', 'updated_at', 'created_by']



class TwistedTowerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TwistedTower
        fields = ['id', 'title', 'base_curve', 'center_point', 'twisted_tower', 'angle', 'height', 'created_at', 'updated_at', 'created_by']