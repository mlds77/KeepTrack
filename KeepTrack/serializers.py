from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    premium = serializers.BooleanField(source='keeptrackuser.premium')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups', 'premium')

    def create(self, validated_data):
        keep_track_user_data = validated_data.pop('keeptrackuser', None)
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_keep_track_user(user, keep_track_user_data)
        return user

    def update(self, instance, validated_data):
        keep_track_user_data = validated_data.pop('keeptrackuser', None)
        self.create_or_update_keep_track_user(instance, keep_track_user_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_keep_track_user(self, user, kt_user_data):
        kt_user, created = KeepTrackUser.objects.get_or_create(user=user, defaults=kt_user_data)
        if not created and kt_user_data is not None:
            super(UserSerializer, self).update(kt_user, kt_user_data)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'url', 'name', 'description', 'date', 'status')


class AllocationSerializer(serializers.HyperlinkedModelSerializer):
    # user = UserSerializer(many=False, read_only=True)
    # event = EventSerializer(many=False, read_only=True)

    class Meta:
        model = Allocation
        fields = ('id', 'url', 'user', 'event', 'attended')