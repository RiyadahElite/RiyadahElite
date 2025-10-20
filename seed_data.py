import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from authapp.models import UserProfile, Tournament, Reward, Game

def seed_database():
    print("Seeding database with sample data...")

    users_created = []

    # Create default users
    default_users = [
        {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
            'role': 'user',
            'points': 150
        },
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'role': 'admin',
            'points': 500
        },
        {
            'username': 'host',
            'email': 'host@example.com',
            'password': 'host123',
            'first_name': 'Host',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
            'role': 'host',
            'points': 300
        }
    ]

    for user_data in default_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser']
            )
            # Ensure UserProfile exists
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = user_data['role']
            profile.points = user_data['points']
            profile.save()
            users_created.append(user)
            print(f"Created user: {user.username}")

    # Tournaments
    tournaments_data = [
        {
            'title': 'FIFA 24 Championship',
            'game': 'FIFA 24',
            'description': 'Compete in the ultimate FIFA 24 tournament for amazing prizes!',
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=9),
            'prize_pool': '$5,000',
            'max_participants': 64,
            'status': 'upcoming'
        },
        {
            'title': 'Call of Duty Warzone Battle',
            'game': 'Call of Duty Warzone',
            'description': 'Battle royale tournament with top players',
            'start_date': datetime.now() + timedelta(days=14),
            'end_date': datetime.now() + timedelta(days=15),
            'prize_pool': '$3,000',
            'max_participants': 100,
            'status': 'upcoming'
        },
        {
            'title': 'Rocket League Pro Series',
            'game': 'Rocket League',
            'description': '3v3 competitive tournament',
            'start_date': datetime.now() + timedelta(days=21),
            'end_date': datetime.now() + timedelta(days=23),
            'prize_pool': '$2,500',
            'max_participants': 24,
            'status': 'upcoming'
        }
    ]

    host_user = User.objects.filter(profile__role='host').first() or User.objects.first()
    for tournament_data in tournaments_data:
        if not Tournament.objects.filter(title=tournament_data['title']).exists():
            tournament = Tournament.objects.create(
                created_by=host_user,
                **tournament_data
            )
            print(f"Created tournament: {tournament.title}")

    # Rewards
    rewards_data = [
        {
            'title': 'Gaming Headset',
            'description': 'Premium wireless gaming headset with 7.1 surround sound',
            'points': 500,
            'category': 'Gaming Gear',
            'stock': 10,
            'is_active': True
        },
        {
            'title': 'Mechanical Keyboard',
            'description': 'RGB mechanical gaming keyboard with custom switches',
            'points': 750,
            'category': 'Gaming Gear',
            'stock': 5,
            'is_active': True
        },
        {
            'title': 'Gaming Mouse',
            'description': 'High-precision gaming mouse with customizable DPI',
            'points': 300,
            'category': 'Gaming Gear',
            'stock': 15,
            'is_active': True
        },
        {
            'title': '$50 Steam Gift Card',
            'description': 'Redeem on Steam for games and content',
            'points': 400,
            'category': 'Gift Cards',
            'stock': 20,
            'is_active': True
        },
        {
            'title': 'Tournament Entry Pass',
            'description': 'Free entry to any premium tournament',
            'points': 200,
            'category': 'Tournament',
            'stock': 50,
            'is_active': True
        }
    ]

    for reward_data in rewards_data:
        if not Reward.objects.filter(title=reward_data['title']).exists():
            reward = Reward.objects.create(**reward_data)
            print(f"Created reward: {reward.title}")

    # Games
    games_data = [
        {
            'title': 'Battle Arena Legends',
            'developer': 'GameDev Studios',
            'genre': 'MOBA',
            'description': 'A fast-paced multiplayer online battle arena game',
            'status': 'testing'
        },
        {
            'title': 'Space Odyssey',
            'developer': 'Indie Games Co',
            'genre': 'Adventure',
            'description': 'Explore the vastness of space in this epic adventure',
            'status': 'pending'
        },
        {
            'title': 'Racing Thunder',
            'developer': 'Speed Games',
            'genre': 'Racing',
            'description': 'High-octane racing with realistic physics',
            'status': 'approved'
        }
    ]

    submitter = User.objects.first()
    for game_data in games_data:
        if not Game.objects.filter(title=game_data['title']).exists():
            game = Game.objects.create(
                submitted_by=submitter,
                **game_data
            )
            print(f"Created game: {game.title}")

    print("\nDatabase seeding completed!")
    print(f"Created {len(users_created)} users")
    print("\nTest credentials:")
    print("  Regular user: testuser / testpass123")
    print("  Admin user: admin / admin123")
    print("  Host user: host / host123")

if __name__ == '__main__':
    seed_database()
