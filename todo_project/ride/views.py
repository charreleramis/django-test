from rest_framework import viewsets
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
    
    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        email = self.request.query_params.get('email', None)
        sort_by = self.request.query_params.get('sort', None)
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('lon', None)
        
        try:
            lat = float(lat) if lat else None
            lon = float(lon) if lon else None
        except (ValueError, TypeError):
            lat = None
            lon = None
        
        return RideService.get_filtered_and_sorted_rides(
            status=status,
            email=email,
            sort_by=sort_by,
            lat=lat,
            lon=lon
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        is_list_result = isinstance(queryset, list)
        
        if is_list_result:
            from rest_framework.pagination import PageNumberPagination
            paginator = PageNumberPagination()
            paginator.page_size = 20
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                data = [ride.serialized for ride in page]
                return paginator.get_paginated_response(data)
            data = [ride.serialized for ride in queryset]
            return Response(data)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                data = [ride.serialized for ride in page]
                return self.get_paginated_response(data)
            data = [ride.serialized for ride in queryset]
            return Response(data)