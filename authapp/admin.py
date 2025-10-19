from django.contrib import admin
from .models import (
    UserProfile, Tournament, TournamentParticipant,
    Reward, UserReward, Game, UserActivity
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'points', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['title', 'game', 'status', 'start_date', 'prize_pool', 'created_by']
    list_filter = ['status', 'game', 'created_at']
    search_fields = ['title', 'game']
    date_hierarchy = 'start_date'

@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'tournament', 'status', 'joined_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__username', 'tournament__title']

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['title', 'points', 'category', 'stock', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'category']

@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward', 'status', 'claimed_at']
    list_filter = ['status', 'claimed_at']
    search_fields = ['user__username', 'reward__title']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'developer', 'genre', 'status', 'submitted_by', 'created_at']
    list_filter = ['status', 'genre', 'created_at']
    search_fields = ['title', 'developer', 'genre']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'points_change', 'status', 'created_at']
    list_filter = ['activity_type', 'status', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
