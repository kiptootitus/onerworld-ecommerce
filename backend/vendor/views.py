
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Vendor
from .serializers import VendorSerializer, VendorUpdateSerializer
from .vendor_handler import VendorHandler

class VendorListView(generics.ListAPIView):
    """
    View to list all vendors.
    """
    queryset = Vendor.objects.all().select_related('user', 'selling_plan', 'residential_address')
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class VendorDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single vendor.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class VendorCreateUpdateView(generics.CreateAPIView):
    """
    View to create or update a vendor.
    """
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        handler = VendorHandler()
        data = {'user': user}
        vendor = handler.create_update_vendor_by_user(data)
        serializer = self.get_serializer(vendor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VendorUpdateView(generics.UpdateAPIView):
    """
    View to update vendor information.
    """
    serializer_class = VendorUpdateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        vendor_id = kwargs.get('id')
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(vendor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(VendorSerializer(vendor).data, status=status.HTTP_200_OK)


class VendorRegistrationStatusView(generics.RetrieveAPIView):
    """
    View to retrieve vendor registration status.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vendor_id = kwargs.get('id')
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=HTTP_400_BAD_REQUEST)

        registration_status = vendor.get_registration_status()
        return Response({'registration_status': registration_status}, status=status.HTTP_200_OK)
