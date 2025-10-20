from django.contrib import admin
from .models import (
    UserProfile, Tournament, TournamentParticipant,
    Reward, UserReward, Game, UserActivity
)

# -----------------------------
# UserProfile Admin
# -----------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'points', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# -----------------------------
# Tournament Admin
# -----------------------------
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'status', 'start_date', 'prize_pool', 'created_by')
    list_filter = ('status', 'game', 'created_at')
    search_fields = ('title', 'game')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'


# -----------------------------
# TournamentParticipant Admin
# -----------------------------
@admin.register(TournamentParticipant)
class TournamentParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'status', 'joined_at')
    list_filter = ('status', 'joined_at')
    search_fields = ('user__username', 'tournament__title')
    ordering = ('-joined_at',)
    date_hierarchy = 'joined_at'


# -----------------------------
# Reward Admin
# -----------------------------
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'category', 'stock', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'category')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# -----------------------------
# UserReward Admin
# -----------------------------
@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'status', 'claimed_at')
    list_filter = ('status', 'claimed_at')
    search_fields = ('user__username', 'reward__title')
    ordering = ('-claimed_at',)
    date_hierarchy = 'claimed_at'


# -----------------------------
# Game Admin
# -----------------------------
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'genre', 'status', 'submitted_by', 'created_at')
    list_filter = ('status', 'genre', 'created_at')
    search_fields = ('title', 'developer', 'genre')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


# -----------------------------
# UserActivity Admin
# -----------------------------
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'points_change', 'status', 'created_at')
    list_filter = ('activity_type', 'status', 'created_at')
    search_fields = ('user__username', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
