from typing import Union, List
from django.db.models import QuerySet
from ride.models import Ride
from ride_event.models import RideEvent
from ride.utils import haversine_distance


class RideService:
    
    @staticmethod
    def _build_queryset(status: str = None, email: str = None, sort_by: str = None) -> QuerySet:
        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('rideevent_set').all()
        
        if status:
            queryset = queryset.filter(status=status)
        
        if email:
            queryset = queryset.filter(id_rider__email__icontains=email)
        
        if sort_by == 'pickup_time':
            queryset = queryset.order_by('pickup_time')
        elif sort_by == '-pickup_time':
            queryset = queryset.order_by('-pickup_time')
        else:
            queryset = queryset.order_by('-pickup_time')
        
        return queryset
    
    @staticmethod
    def _sort_by_distance(rides: List[Ride], lat: float, lon: float, reverse: bool = False) -> List[Ride]:
        rides_with_distance = [
            (ride, haversine_distance(lat, lon, ride.pickup_latitude, ride.pickup_longitude))
            for ride in rides
        ]
        rides_with_distance.sort(key=lambda x: x[1], reverse=reverse)
        return [ride for ride, _ in rides_with_distance]
    
    @classmethod
    def get_base_queryset(cls) -> QuerySet:
        return Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('rideevent_set').all()
    
    @classmethod
    def get_filtered_and_sorted_rides(cls, status: str = None, email: str = None, 
                                      sort_by: str = None, lat: float = None, lon: float = None,
                                      page: int = 1, page_size: int = 20) -> dict:
        offset = (page - 1) * page_size
        
        queryset = cls._build_queryset(status=status, email=email, sort_by=sort_by)
        
        if sort_by in ['distance', '-distance'] and lat is not None and lon is not None:
            all_rides = list(queryset)
            sorted_rides = cls._sort_by_distance(all_rides, lat, lon, reverse=(sort_by == '-distance'))
            total_count = len(sorted_rides)
            paginated_rides = sorted_rides[offset:offset + page_size]
            return {
                'results': paginated_rides,
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
            }
        
        total_count = queryset.count()
        rides = list(queryset[offset:offset + page_size])
        
        return {
            'results': rides,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
        }
    
    @staticmethod
    def get_rides_with_duration(page: int = 1, page_size: int = 20) -> dict:
        offset = (page - 1) * page_size
        
        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('rideevent_set').all().order_by('-pickup_time')
        total_count = queryset.count()
        
        rides = list(queryset[offset:offset + page_size])
        
        ride_ids = [ride.id_ride for ride in rides]
        all_events = RideEvent.objects.filter(id_ride__in=ride_ids).select_related('id_ride')
        
        events_by_ride = {}
        for event in all_events:
            if event.id_ride_id not in events_by_ride:
                events_by_ride[event.id_ride_id] = {'pickup': None, 'dropoff': None}
            if event.description == 'Status changed to pickup':
                events_by_ride[event.id_ride_id]['pickup'] = event
            elif event.description == 'Status changed to dropoff':
                events_by_ride[event.id_ride_id]['dropoff'] = event
        
        results = []
        for ride in rides:
            ride_events = events_by_ride.get(ride.id_ride, {'pickup': None, 'dropoff': None})
            pickup_event = ride_events['pickup']
            dropoff_event = ride_events['dropoff']
            
            ride_data = ride.serialized
            
            if pickup_event and dropoff_event:
                duration = dropoff_event.created_at - pickup_event.created_at
                ride_data['trip_duration_minutes'] = int(duration.total_seconds() / 60)
            else:
                ride_data['trip_duration_minutes'] = None
            
            ride_data['pickup_event_time'] = pickup_event.created_at.isoformat() if pickup_event else None
            ride_data['dropoff_event_time'] = dropoff_event.created_at.isoformat() if dropoff_event else None
            
            results.append(ride_data)
        
        return {
            'results': results,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
        }
