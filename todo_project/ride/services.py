from typing import Union, List
from django.db import connection
from django.db.models import QuerySet
from ride.models import Ride
from ride.utils import haversine_distance


class RideService:
    
    @staticmethod
    def _build_sql_query(status: str = None, email: str = None, sort_by: str = None) -> tuple:
        base_query = """
            SELECT DISTINCT r.id_ride
            FROM ride r
            INNER JOIN user rider ON r.id_rider = rider.id_user
            INNER JOIN user driver ON r.id_driver = driver.id_user
            WHERE 1=1
        """
        params = []
        
        if status:
            base_query += " AND r.status = %s"
            params.append(status)
        
        if email:
            base_query += " AND rider.email LIKE %s"
            params.append(f'%{email}%')
        
        if sort_by == 'pickup_time':
            base_query += " ORDER BY r.pickup_time ASC"
        elif sort_by == '-pickup_time':
            base_query += " ORDER BY r.pickup_time DESC"
        else:
            base_query += " ORDER BY r.pickup_time DESC"
        
        return base_query, params
    
    @staticmethod
    def _execute_sql_query(query: str, params: list) -> List[Ride]:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            ride_ids = [row[0] for row in cursor.fetchall()]
            
            if not ride_ids:
                return []
            
            rides = list(Ride.objects.select_related('id_rider', 'id_driver')
                        .prefetch_related('rideevent_set')
                        .filter(id_ride__in=ride_ids))
            
            ride_dict = {ride.id_ride: ride for ride in rides}
            ordered_rides = [ride_dict[rid] for rid in ride_ids if rid in ride_dict]
            
            return ordered_rides
    
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
                                      sort_by: str = None, lat: float = None, lon: float = None) -> Union[QuerySet, list]:
        if sort_by in ['distance', '-distance'] and lat is not None and lon is not None:
            query, params = cls._build_sql_query(status=status, email=email)
            rides = cls._execute_sql_query(query, params)
            return cls._sort_by_distance(rides, lat, lon, reverse=(sort_by == '-distance'))
        
        query, params = cls._build_sql_query(status=status, email=email, sort_by=sort_by)
        return cls._execute_sql_query(query, params)
