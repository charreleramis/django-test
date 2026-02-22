from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from user.models import User
from ride.models import Ride
from ride_event.models import RideEvent


class Command(BaseCommand):
    help = 'Seed sample data for Ride and RideEvent models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            RideEvent.objects.all().delete()
            Ride.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

        users = User.objects.all()
        if users.count() < 5:
            self.stdout.write(self.style.WARNING('Creating sample users...'))
            sample_users = [
                {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'phone_number': '1234567890', 'role': 'user'},
                {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane.smith@example.com', 'phone_number': '1234567891', 'role': 'user'},
                {'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike.johnson@example.com', 'phone_number': '1234567892', 'role': 'driver'},
                {'first_name': 'Sarah', 'last_name': 'Williams', 'email': 'sarah.williams@example.com', 'phone_number': '1234567893', 'role': 'driver'},
                {'first_name': 'David', 'last_name': 'Brown', 'email': 'david.brown@example.com', 'phone_number': '1234567894', 'role': 'driver'},
            ]
            
            for user_data in sample_users:
                if not User.objects.filter(email=user_data['email']).exists():
                    password = 'password123'
                    user = User.objects.create(
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        email=user_data['email'],
                        phone_number=user_data['phone_number'],
                        role=user_data['role'],
                        password=''
                    )
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Created user: {user.email} with password: {password}'))
            
            users = User.objects.all()

        drivers = users.filter(role='driver')
        if drivers.count() == 0:
            drivers = users.filter(role__in=['driver', 'user'])[:3]
        
        riders = users.exclude(id_user__in=drivers.values_list('id_user', flat=True))
        if riders.count() == 0:
            riders = users.filter(role__in=['user', 'passenger'])[:5]
        if riders.count() == 0:
            riders = users.exclude(role='admin')[:5]

        self.stdout.write(self.style.SUCCESS('Creating sample rides...'))
        
        statuses = ['en-route', 'pickup', 'dropoff', 'completed', 'cancelled']
        
        sample_locations = [
            {'pickup': (40.7128, -74.0060), 'dropoff': (40.7589, -73.9851)},
            {'pickup': (40.7505, -73.9934), 'dropoff': (40.7282, -73.7949)},
            {'pickup': (40.7614, -73.9776), 'dropoff': (40.6782, -73.9442)},
            {'pickup': (40.7489, -73.9680), 'dropoff': (40.6892, -74.0445)},
            {'pickup': (40.7282, -73.7949), 'dropoff': (40.7128, -74.0060)},
        ]

        rides_created = 0
        for i in range(10):
            if riders.count() == 0 or drivers.count() == 0:
                break
                
            rider = random.choice(riders)
            driver = random.choice(drivers)
            
            if rider.id_user == driver.id_user:
                continue
            
            location = random.choice(sample_locations)
            status = random.choice(statuses)
            
            pickup_time = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            ride = Ride.objects.create(
                status=status,
                id_rider=rider,
                id_driver=driver,
                pickup_latitude=location['pickup'][0],
                pickup_longitude=location['pickup'][1],
                dropoff_latitude=location['dropoff'][0],
                dropoff_longitude=location['dropoff'][1],
                pickup_time=pickup_time
            )
            rides_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'Created ride #{ride.id_ride}: {rider.first_name} -> {driver.first_name} ({status})'))

        self.stdout.write(self.style.SUCCESS('Creating sample ride events...'))
        
        rides = Ride.objects.all()
        event_descriptions = [
            'Ride requested',
            'Driver assigned',
            'Driver on the way',
            'Driver arrived at pickup location',
            'Passenger picked up',
            'Ride in progress',
            'Arrived at destination',
            'Ride completed',
            'Payment processed',
            'Ride cancelled by passenger',
            'Ride cancelled by driver',
        ]
        
        events_created = 0
        for ride in rides:
            num_events = random.randint(2, 5)
            event_time = ride.pickup_time
            
            for j in range(num_events):
                description = random.choice(event_descriptions)
                event_time = event_time + timedelta(minutes=random.randint(5, 30))
                
                if event_time > timezone.now():
                    event_time = timezone.now() - timedelta(minutes=random.randint(1, 60))
                
                ride_event = RideEvent(
                    id_ride=ride,
                    description=description
                )
                ride_event.save()
                RideEvent.objects.filter(id_ride_event=ride_event.id_ride_event).update(created_at=event_time)
                
                events_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {events_created} ride events.'))

        self.stdout.write(self.style.SUCCESS(f'\nSeeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total rides: {Ride.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total ride events: {RideEvent.objects.count()}'))
