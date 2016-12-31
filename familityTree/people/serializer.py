# coding: utf-8
from rest_framework import serializers
from .models import People


class FamilyTreeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    birthday = serializers.DateField(required=False)
    sex = serializers.BooleanField(required=False)
    dieday = serializers.DateField(required=False)
    display = serializers.BooleanField()
    generation = serializers.IntegerField()
    marriage_flg = serializers.BooleanField(required=False)
    parent_node = serializers.CharField(required=False)
    node1 = serializers.CharField(required=False)
    node2 = serializers.CharField(required=False)


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'
