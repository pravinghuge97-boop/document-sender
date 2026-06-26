"""
Seed script — creates 10 test users.
Run from the backend/ directory:
    python seed.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

USERS = [
    {"username": "alice",    "email": "alice@test.com",    "password": "password123", "first_name": "Alice",    "last_name": "Johnson"},
    {"username": "bob",      "email": "bob@test.com",      "password": "password123", "first_name": "Bob",      "last_name": "Smith"},
    {"username": "charlie",  "email": "charlie@test.com",  "password": "password123", "first_name": "Charlie",  "last_name": "Brown"},
    {"username": "diana",    "email": "diana@test.com",    "password": "password123", "first_name": "Diana",    "last_name": "Prince"},
    {"username": "eve",      "email": "eve@test.com",      "password": "password123", "first_name": "Eve",      "last_name": "Adams"},
    {"username": "frank",    "email": "frank@test.com",    "password": "password123", "first_name": "Frank",    "last_name": "Miller"},
    {"username": "grace",    "email": "grace@test.com",    "password": "password123", "first_name": "Grace",    "last_name": "Lee"},
    {"username": "henry",    "email": "henry@test.com",    "password": "password123", "first_name": "Henry",    "last_name": "Wilson"},
    {"username": "isabella", "email": "isabella@test.com", "password": "password123", "first_name": "Isabella", "last_name": "Moore"},
    {"username": "jack",     "email": "jack@test.com",     "password": "password123", "first_name": "Jack",     "last_name": "Taylor"},
]

print("\n=== Seeding Users ===\n")
created = 0
skipped = 0

for u in USERS:
    if User.objects.filter(email=u["email"]).exists():
        print(f"  [SKIP]    {u['email']} already exists")
        skipped += 1
    else:
        user = User.objects.create_user(
            username=u["username"],
            email=u["email"],
            password=u["password"],
            first_name=u["first_name"],
            last_name=u["last_name"],
        )
        print(f"  [CREATED] {u['email']}  (password: {u['password']})")
        created += 1

print(f"\n✅ Done — {created} created, {skipped} skipped.")
print(f"   Total users in DB: {User.objects.count()}\n")
print("Login credentials for all new users:")
print("  Password: password123\n")
