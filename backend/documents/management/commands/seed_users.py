from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed database with test users'

    def handle(self, *args, **options):
        # users = [
        #     {
        #         'email': 'owner@test.com',
        #         'username': 'owner',
        #         'password': 'Password123'
        #     },
        #     {
        #         'email': 'collaborator@test.com',
        #         'username': 'collaborator',
        #         'password': 'Password123'
        #     }
        # ]
        users = [
            {
            'email': 'alex@test.com',
            'username': 'alex',
            'password': 'Password123'
            },
            {
            'email': 'emma@test.com',
            'username': 'emma',
            'password': 'Password123'
            },
            {
            'email': 'john@test.com',
            'username': 'john',
            'password': 'Password123'
            },
            {
            'email': 'sophia@test.com',
            'username': 'sophia',
            'password': 'Password123'
            },
            {
            'email': 'michael@test.com',
            'username': 'michael',
            'password': 'Password123'
            },
            {
            'email': 'olivia@test.com',
            'username': 'olivia',
            'password': 'Password123'
            },
            {
            'email': 'daniel@test.com',
            'username': 'daniel',
            'password': 'Password123'
            },
            {
            'email': 'ava@test.com',
            'username': 'ava',
            'password': 'Password123'
            },
            {
            'email': 'william@test.com',
            'username': 'william',
            'password': 'Password123'
            },
            {
            'email': 'mia@test.com',
            'username': 'mia',
            'password': 'Password123'
            }
            ]


        for user_data in users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password']
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user_data["email"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user_data["email"]}')
                )
