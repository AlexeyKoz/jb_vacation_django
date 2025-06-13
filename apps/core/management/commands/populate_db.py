from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import Country
from apps.vacations.models import Vacation
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

COUNTRIES = [
    'France', 'Italy', 'Spain', 'Greece', 'Germany',
    'United Kingdom', 'Japan', 'Thailand', 'Australia', 'United States',
    'Canada', 'Brazil', 'South Africa', 'Egypt', 'India'
]

VACATION_DESCRIPTIONS = [
    "Experience the rich culture and history of {country}. From ancient landmarks to modern attractions, this vacation offers something for everyone.",
    "Discover the natural beauty of {country}. Enjoy breathtaking landscapes, pristine beaches, and unforgettable adventures.",
    "Immerse yourself in the vibrant atmosphere of {country}. Taste local cuisine, explore charming streets, and create lasting memories.",
    "Escape to the paradise of {country}. Relax on beautiful beaches, enjoy water sports, and experience tropical bliss.",
    "Explore the wonders of {country}. Visit famous landmarks, museums, and experience the local way of life."
]


class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating admin user...')
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin1234',
            first_name='Admin',
            last_name='User'
        )
        self.stdout.write(self.style.SUCCESS(
            'Admin user created successfully'))

        self.stdout.write('Creating regular user...')
        user = User.objects.create_user(
            email='user@example.com',
            password='user1234',
            first_name='Regular',
            last_name='User'
        )
        self.stdout.write(self.style.SUCCESS(
            'Regular user created successfully'))

        self.stdout.write('Creating countries...')
        countries = []
        for country_name in COUNTRIES:
            country, created = Country.objects.get_or_create(name=country_name)
            countries.append(country)
        self.stdout.write(self.style.SUCCESS(
            f'Created {len(countries)} countries'))

        self.stdout.write('Creating vacations...')
        start_date = timezone.now().date()
        for i in range(12):
            country = random.choice(countries)
            vacation_start = start_date + timedelta(days=i*30)
            vacation_end = vacation_start + \
                timedelta(days=random.randint(5, 14))
            price = random.randint(500, 9500)
            description = random.choice(
                VACATION_DESCRIPTIONS).format(country=country.name)

            Vacation.objects.create(
                country=country,
                description=description,
                start_date=vacation_start,
                end_date=vacation_end,
                price=price
            )
        self.stdout.write(self.style.SUCCESS('Created 12 vacations'))

        self.stdout.write(self.style.SUCCESS(
            'Database populated successfully'))
