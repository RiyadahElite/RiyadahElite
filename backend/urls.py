from django.urls import path, re_path
from authapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth APIs
    path('auth/register/', views.register_view),
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/user/', views.user_view),

    # Tournament APIs
    path('tournaments/', views.tournament_list),
    path('tournaments/<int:pk>/', views.tournament_detail),
    path('tournaments/<int:pk>/join/', views.tournament_join),
    path('tournaments/<int:pk>/leave/', views.tournament_leave),
    path('tournaments/user/', views.user_tournaments),

    # Reward APIs
    path('rewards/', views.reward_list),
    path('rewards/claim/', views.reward_claim),
    path('rewards/user/', views.user_rewards),

    # Game APIs
    path('games/', views.game_list),
    path('games/<int:pk>/status/', views.game_update_status),

    # Dashboard
    path('dashboard/', views.dashboard_data),

    # Catch-all: serves React frontend
    re_path(r'^.*$', views.FrontendAppView.as_view(), name='frontend'),
]

# Serve React assets in development
if settings.DEBUG:
    urlpatterns += static(
        '/assets/',  # matches React build
        document_root=settings.BASE_DIR / 'frontend' / 'dist' / 'assets'
    )
