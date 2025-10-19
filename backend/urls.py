from django.contrib import admin
from django.urls import path, include
from authapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/tournaments/', views.tournament_list, name='tournament-list'),
    path('api/tournaments/<int:pk>/', views.tournament_detail, name='tournament-detail'),
    path('api/tournaments/<int:pk>/join/', views.tournament_join, name='tournament-join'),
    path('api/tournaments/<int:pk>/leave/', views.tournament_leave, name='tournament-leave'),
    path('api/tournaments/user/', views.user_tournaments, name='user-tournaments'),
    path('api/rewards/', views.reward_list, name='reward-list'),
    path('api/rewards/claim/', views.reward_claim, name='reward-claim'),
    path('api/rewards/user/', views.user_rewards, name='user-rewards'),
    path('api/games/', views.game_list, name='game-list'),
    path('api/games/<int:pk>/status/', views.game_update_status, name='game-update-status'),
    path('api/dashboard/', views.dashboard_data, name='dashboard-data'),
]
