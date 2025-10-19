from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import (
    UserProfile, Tournament, TournamentParticipant,
    Reward, UserReward, Game, UserActivity
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role', 'avatar', 'points', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.CharField(source='profile.role', read_only=True)
    avatar = serializers.URLField(source='profile.avatar', read_only=True, allow_null=True)
    points = serializers.IntegerField(source='profile.points', read_only=True)
    created_at = serializers.DateTimeField(source='profile.created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='profile.updated_at', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'first_name', 'last_name', 'role', 'avatar', 'points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserActivity.objects.create(
            user=user,
            activity_type='registration',
            description=f"User {user.username} registered",
            points_change=0
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")

class TournamentSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tournament
        fields = ['id', 'title', 'game', 'description', 'start_date', 'end_date',
                  'prize_pool', 'max_participants', 'status', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

class TournamentParticipantSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(read_only=True)

    class Meta:
        model = TournamentParticipant
        fields = ['id', 'user_id', 'tournament_id', 'tournament', 'status', 'joined_at']
        read_only_fields = ['id', 'user_id', 'joined_at']

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'title', 'description', 'points', 'category',
                  'image_url', 'stock', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserRewardSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(read_only=True)

    class Meta:
        model = UserReward
        fields = ['id', 'user_id', 'reward_id', 'reward', 'status', 'claimed_at']
        read_only_fields = ['id', 'user_id', 'claimed_at']

class GameSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'title', 'developer', 'genre', 'description',
                  'status', 'image_url', 'submitted_by', 'created_at']
        read_only_fields = ['id', 'submitted_by', 'created_at']

class UserActivitySerializer(serializers.ModelSerializer):
    tournament = serializers.SerializerMethodField()
    reward = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = ['id', 'user_id', 'tournament_id', 'reward_id', 'activity_type',
                  'description', 'points_change', 'status', 'created_at', 'tournament', 'reward']
        read_only_fields = ['id', 'user_id', 'created_at']

    def get_tournament(self, obj):
        if obj.tournament:
            return {'title': obj.tournament.title}
        return None

    def get_reward(self, obj):
        if obj.reward:
            return {'title': obj.reward.title}
        return None
