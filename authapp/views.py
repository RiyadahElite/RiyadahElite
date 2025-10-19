from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.db.models import Count, Q
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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        UserActivity.objects.create(
            user=user,
            activity_type='login',
            description=f"User {user.username} logged in",
            points_change=0
        )
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    return Response({
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tournament_list(request):
    if request.method == 'GET':
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            tournament = serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_detail(request, pk):
    try:
        tournament = Tournament.objects.get(pk=pk)
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tournament_join(request, pk):
    try:
        tournament = Tournament.objects.get(pk=pk)

        if TournamentParticipant.objects.filter(user=request.user, tournament=tournament).exists():
            return Response({'error': 'Already joined this tournament'}, status=status.HTTP_400_BAD_REQUEST)

        participant = TournamentParticipant.objects.create(
            user=request.user,
            tournament=tournament
        )

        UserActivity.objects.create(
            user=request.user,
            tournament=tournament,
            activity_type='tournament_join',
            description=f"Joined tournament: {tournament.title}",
            points_change=10
        )

        request.user.profile.points += 10
        request.user.profile.save()

        return Response({'message': 'Successfully joined tournament'}, status=status.HTTP_201_CREATED)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tournament_leave(request, pk):
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

        request.user.profile.points = max(0, request.user.profile.points - 10)
        request.user.profile.save()

        return Response({'message': 'Successfully left tournament'}, status=status.HTTP_200_OK)
    except Tournament.DoesNotExist:
        return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
    except TournamentParticipant.DoesNotExist:
        return Response({'error': 'Not enrolled in this tournament'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tournaments(request):
    participations = TournamentParticipant.objects.filter(user=request.user)
    serializer = TournamentParticipantSerializer(participations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reward_list(request):
    rewards = Reward.objects.filter(is_active=True)
    serializer = RewardSerializer(rewards, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reward_claim(request):
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

        user_reward = UserReward.objects.create(
            user=request.user,
            reward=reward
        )

        request.user.profile.points -= reward.points
        request.user.profile.save()

        reward.stock -= 1
        reward.save()

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
    user_rewards = UserReward.objects.filter(user=request.user)
    serializer = UserRewardSerializer(user_rewards, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def game_list(request):
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

            request.user.profile.points += 25
            request.user.profile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def game_update_status(request, pk):
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    user = request.user

    tournaments = TournamentParticipant.objects.filter(user=user)
    rewards = UserReward.objects.filter(user=user)
    activities = UserActivity.objects.filter(user=user)[:20]

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
