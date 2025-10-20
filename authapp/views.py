# authapp/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.db.models import F
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import View
from django.http import HttpResponse
import os
from django.conf import settings  


from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    TournamentSerializer, TournamentParticipantSerializer,
    RewardSerializer, UserRewardSerializer,
    GameSerializer, UserActivitySerializer
)
from .models import (
    Tournament, TournamentParticipant,
    Reward, UserReward, Game, UserActivity
)

# -------------------------------------------------------------------
# 🔐 AUTHENTICATION HELPERS
# -------------------------------------------------------------------

def get_tokens_for_user(user):
    """
    Helper to generate JWT refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class FrontendAppView(View):
    """
    Serves the compiled React app's index.html.
    """
    def get(self, request, *args, **kwargs):
        index_file = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'index.html')
        try:
            with open(index_file, encoding='utf-8') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "React build not found. Run `npm run build` in the frontend directory.",
                status=501,
            )
        
# -------------------------------------------------------------------
# 👤 USER AUTHENTICATION VIEWS
# -------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user and automatically log them in.
    Returns JWT tokens and user data.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': tokens,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login user and return JWT tokens.
    Also logs user activity.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)

        # Record user activity
        UserActivity.objects.create(
            user=user,
            activity_type='login',
            description=f"User {user.username} logged in",
            points_change=0
        )

        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': tokens,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Log the user out and record the activity.
    """
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    """
    Fetch current logged-in user details.
    """
    return Response({'user': UserSerializer(request.user).data}, status=status.HTTP_200_OK)

# -------------------------------------------------------------------
# 🏆 TOURNAMENT VIEWS
# -------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tournament_list(request):
    """
    GET - List all tournaments.
    POST - Create a new tournament.
    """
    if request.method == 'GET':
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_detail(request, pk):
    """
    Get tournament details by ID.
    """
    try:
        tournament = Tournament.objects.get(pk=pk)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tournament_join(request, pk):
    """
    Join a tournament and earn points.
    """
    try:
        tournament = Tournament.objects.get(pk=pk)

        if TournamentParticipant.objects.filter(user=request.user, tournament=tournament).exists():
            return Response({'error': 'Already joined this tournament'}, status=status.HTTP_400_BAD_REQUEST)

        TournamentParticipant.objects.create(user=request.user, tournament=tournament)

        UserActivity.objects.create(
            user=request.user,
            tournament=tournament,
            activity_type='tournament_join',
            description=f"Joined tournament: {tournament.title}",
            points_change=10
        )

        request.user.profile.points = F('points') + 10
        request.user.profile.save()
        request.user.profile.refresh_from_db()

        return Response({'message': 'Successfully joined tournament'}, status=status.HTTP_201_CREATED)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tournament_leave(request, pk):
    """
    Leave a tournament and lose points.
    """
    try:
        tournament = Tournament.objects.get(pk=pk)
        participant = TournamentParticipant.objects.get(user=request.user, tournament=tournament)
        participant.delete()

        UserActivity.objects.create(
            user=request.user,
            tournament=tournament,
            activity_type='tournament_leave',
            description=f"Left tournament: {tournament.title}",
            points_change=-10
        )

        request.user.profile.points = F('points') - 10
        request.user.profile.save()
        request.user.profile.refresh_from_db()

        return Response({'message': 'Successfully left tournament'}, status=status.HTTP_200_OK)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
    except TournamentParticipant.DoesNotExist:
        return Response({'error': 'Not enrolled in this tournament'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tournaments(request):
    """
    List tournaments the user is part of.
    """
    participations = TournamentParticipant.objects.filter(user=request.user)
    serializer = TournamentParticipantSerializer(participations, many=True)
    return Response(serializer.data)

# -------------------------------------------------------------------
# 🎁 REWARD SYSTEM
# -------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reward_list(request):
    """
    List all active rewards.
    """
    rewards = Reward.objects.filter(is_active=True)
    serializer = RewardSerializer(rewards, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reward_claim(request):
    """
    Claim a reward if the user has enough points.
    """
    reward_id = request.data.get('rewardId')

    if not reward_id:
        return Response({'error': 'Reward ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        reward = Reward.objects.get(pk=reward_id)

        if not reward.is_active:
            return Response({'error': 'Reward is not active'}, status=status.HTTP_400_BAD_REQUEST)

        if reward.stock <= 0:
            return Response({'error': 'Reward is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.profile.points < reward.points:
            return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)

        UserReward.objects.create(user=request.user, reward=reward)

        request.user.profile.points = F('points') - reward.points
        request.user.profile.save()
        request.user.profile.refresh_from_db()

        reward.stock = F('stock') - 1
        reward.save()
        reward.refresh_from_db()

        UserActivity.objects.create(
            user=request.user,
            reward=reward,
            activity_type='reward_claim',
            description=f"Claimed reward: {reward.title}",
            points_change=-reward.points
        )

        return Response({'message': 'Reward claimed successfully'}, status=status.HTTP_201_CREATED)
    except Reward.DoesNotExist:
        return Response({'error': 'Reward not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_rewards(request):
    """
    List all rewards claimed by the user.
    """
    user_rewards = UserReward.objects.filter(user=request.user)
    serializer = UserRewardSerializer(user_rewards, many=True)
    return Response(serializer.data)

# -------------------------------------------------------------------
# 🕹️ GAME SUBMISSION
# -------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def game_list(request):
    """
    GET - List all submitted games.
    POST - Submit a new game (awards points).
    """
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save(submitted_by=request.user)

            UserActivity.objects.create(
                user=request.user,
                activity_type='points_earned',
                description=f"Submitted game: {game.title}",
                points_change=25
            )

            request.user.profile.points = F('points') + 25
            request.user.profile.save()
            request.user.profile.refresh_from_db()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def game_update_status(request, pk):
    """
    Update game status (e.g., Approved, Pending, Rejected).
    """
    try:
        game = Game.objects.get(pk=pk)
        new_status = request.data.get('status')

        if new_status not in dict(Game.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        game.status = new_status
        game.save()

        return Response({'message': 'Game status updated successfully'}, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

# -------------------------------------------------------------------
# 📊 DASHBOARD VIEW
# -------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """
    Returns user dashboard data: tournaments, rewards, activities, and stats.
    """
    user = request.user

    tournaments = TournamentParticipant.objects.filter(user=user)
    rewards = UserReward.objects.filter(user=user)
    activities = UserActivity.objects.filter(user=user).order_by('-created_at')[:20]

    total_tournaments = tournaments.count()
    total_rewards = rewards.count()
    total_points = user.profile.points

    return Response({
        'user': UserSerializer(user).data,
        'tournaments': TournamentParticipantSerializer(tournaments, many=True).data,
        'rewards': UserRewardSerializer(rewards, many=True).data,
        'activity': UserActivitySerializer(activities, many=True).data,
        'stats': {
            'totalTournaments': total_tournaments,
            'totalRewards': total_rewards,
            'totalPoints': total_points,
        }
    })
