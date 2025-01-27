from django.urls import path
from .views import (
    VendorListView,
    VendorDetailView,
    VendorCreateUpdateView,
    VendorUpdateView,
    VendorRegistrationStatusView,
)

urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/create-update/', VendorCreateUpdateView.as_view(), name='vendor-create-update'),
    path('vendors/<int:id>/update/', VendorUpdateView.as_view(), name='vendor-update'),
    path('vendors/<int:id>/registration-status/', VendorRegistrationStatusView.as_view(), name='vendor-registration-status'),
]
