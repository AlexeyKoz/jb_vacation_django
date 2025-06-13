from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from apps.core.models import Country
from apps.vacations.models import Vacation
from datetime import timedelta
import random
import os
import requests
from tempfile import NamedTemporaryFile
from pathlib import Path


class Command(BaseCommand):
    help = 'Generates sample vacations with images'

    VACATION_DATA = [
        {
            'country': 'France',
            'description': 'Experience the magic of Paris with its iconic Eiffel Tower, world-class museums, and charming cafes. Enjoy the romantic atmosphere and rich cultural heritage.',
            'image_url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800'
        },
        {
            'country': 'Italy',
            'description': 'Discover the eternal city of Rome with its ancient ruins, Vatican City, and delicious Italian cuisine. Immerse yourself in history and art.',
            'image_url': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800'
        },
        {
            'country': 'Spain',
            'description': 'Enjoy the vibrant city of Barcelona with its unique architecture, beautiful beaches, and lively atmosphere. Perfect for art lovers and food enthusiasts.',
            'image_url': 'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800'
        },
        {
            'country': 'Greece',
            'description': 'Visit the stunning Santorini with its white-washed buildings, blue domes, and breathtaking sunsets. A perfect romantic getaway.',
            'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800'
        },
        {
            'country': 'Japan',
            'description': 'Explore Tokyo, a fascinating blend of traditional culture and cutting-edge technology. Experience unique cuisine and vibrant city life.',
            'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800'
        },
        {
            'country': 'Thailand',
            'description': 'Relax in Phuket with its pristine beaches, crystal-clear waters, and luxurious resorts. Perfect for beach lovers and water sports enthusiasts.',
            'image_url': 'https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800'
        },
        {
            'country': 'Australia',
            'description': 'Discover Sydney with its iconic Opera House, beautiful harbor, and stunning beaches. Experience the perfect blend of city and nature.',
            'image_url': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800'
        },
        {
            'country': 'United States',
            'description': 'Visit New York City, the city that never sleeps. Experience world-famous landmarks, Broadway shows, and diverse cultural attractions.',
            'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800'
        },
        {
            'country': 'Canada',
            'description': 'Explore Vancouver with its stunning natural beauty, diverse culture, and outdoor activities. Perfect for nature lovers and adventure seekers.',
            'image_url': 'https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=800'
        },
        {
            'country': 'Brazil',
            'description': 'Experience Rio de Janeiro with its famous beaches, vibrant culture, and iconic Christ the Redeemer statue. A perfect mix of nature and city life.',
            'image_url': 'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800'
        },
        {
            'country': 'South Africa',
            'description': 'Visit Cape Town with its stunning Table Mountain, beautiful beaches, and rich cultural heritage. Perfect for nature and adventure lovers.',
            'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800'
        },
        {
            'country': 'Egypt',
            'description': 'Discover Cairo with its ancient pyramids, rich history, and vibrant culture. A perfect destination for history enthusiasts.',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268ace1d5ccb?w=800'
        },
        {
            'country': 'India',
            'description': 'Experience the magic of Jaipur with its stunning palaces, rich culture, and vibrant markets. Perfect for cultural exploration.',
            'image_url': 'https://images.unsplash.com/photo-1532377610265-d67456d7b175?w=800'
        },
        {
            'country': 'United Kingdom',
            'description': 'Visit London with its iconic landmarks, rich history, and diverse cultural attractions. Perfect for history and culture lovers.',
            'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800'
        },
        {
            'country': 'Germany',
            'description': 'Explore Berlin with its rich history, vibrant art scene, and diverse cultural attractions. Perfect for history and culture enthusiasts.',
            'image_url': 'https://images.unsplash.com/photo-1599946347371-68eb71b16afc?w=800'
        }
    ]

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating vacations with images...')

        # Create media directory if it doesn't exist
        media_dir = Path('media/vacations')
        media_dir.mkdir(parents=True, exist_ok=True)

        start_date = timezone.now().date()

        for i, data in enumerate(self.VACATION_DATA):
            try:
                # Get or create country
                country, created = Country.objects.get_or_create(
                    name=data['country'])

                # Calculate dates
                vacation_start = start_date + timedelta(days=i*30)
                vacation_end = vacation_start + \
                    timedelta(days=random.randint(5, 14))

                # Generate price between 500 and 9500
                price = random.randint(500, 9500)

                # Create vacation
                vacation = Vacation.objects.create(
                    country=country,
                    description=data['description'],
                    start_date=vacation_start,
                    end_date=vacation_end,
                    price=price
                )

                # Download and save image
                response = requests.get(data['image_url'])
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()

                    # Save the image
                    vacation.image.save(
                        f"{country.name.lower().replace(' ', '_')}.jpg",
                        File(img_temp),
                        save=True
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created vacation to {country.name}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Could not download image for {country.name}'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating vacation for {data["country"]}: {str(e)}'
                    )
                )

        self.stdout.write(self.style.SUCCESS(
            'Successfully created all vacations'))
