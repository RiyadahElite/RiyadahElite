import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from authapp.models import (
    UserProfile, Tournament, Reward, Game
)

def seed_database():
    print("Seeding database with sample data...")

    users_created = []

    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        user.profile.points = 150
        user.profile.save()
        users_created.append(user)
        print(f"Created user: {user.username}")

    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True
        )
        admin_user.profile.role = 'admin'
        admin_user.profile.points = 500
        admin_user.profile.save()
        users_created.append(admin_user)
        print(f"Created admin user: {admin_user.username}")

    if not User.objects.filter(username='host').exists():
        host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='host123',
            first_name='Host',
            last_name='User'
        )
        host_user.profile.role = 'host'
        host_user.profile.points = 300
        host_user.profile.save()
        users_created.append(host_user)
        print(f"Created host user: {host_user.username}")

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
