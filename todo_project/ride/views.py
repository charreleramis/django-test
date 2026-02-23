from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ride.models import Ride
from ride.serializers import RideSerializer
from ride.services import RideService
from user.permissions import IsAdminRole


class RideViewSet(viewsets.ModelViewSet):
    queryset = RideService.get_base_queryset()
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id_ride'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance.serialized)
    
    def list(self, request, *args, **kwargs):
        status = request.query_params.get('status', None)
        email = request.query_params.get('email', None)
        sort_by = request.query_params.get('sort', None)
        lat = request.query_params.get('lat', None)
        lon = request.query_params.get('lon', None)
        
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10
        
        try:
            lat = float(lat) if lat else None
            lon = float(lon) if lon else None
        except (ValueError, TypeError):
            lat = None
            lon = None
        
        result = RideService.get_filtered_and_sorted_rides(
            status=status,
            email=email,
            sort_by=sort_by,
            lat=lat,
            lon=lon,
            page=page,
            page_size=page_size
        )
        
        data = [ride.serialized for ride in result['results']]
        
        return Response({
            'count': result['count'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages'],
            'next': f"?page={page + 1}&page_size={page_size}" if page < result['total_pages'] else None,
            'previous': f"?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'results': data
        })
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAdminRole])
    def with_duration(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10
        
        result = RideService.get_rides_with_duration(page=page, page_size=page_size)
        
        return Response({
            'count': result['count'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages'],
            'next': f"?page={page + 1}&page_size={page_size}" if page < result['total_pages'] else None,
            'previous': f"?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'results': result['results']
        }, status=status.HTTP_200_OK)