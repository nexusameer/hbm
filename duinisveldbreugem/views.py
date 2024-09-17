from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.

class InvoiceViewSet(ReadOnlyModelViewSet):
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.InvoiceSerializer
    filter_fields = ('invoice_number',)

class InvoiceItemViewSet(ReadOnlyModelViewSet):
    queryset = models.InvoiceItem.objects.all()
    serializer_class = serializers.InvoiceItemSerializer