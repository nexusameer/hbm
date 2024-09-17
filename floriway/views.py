from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.


class FloriwayViewSet(ReadOnlyModelViewSet):
    queryset = models.Floriway.objects.all()
    serializer_class = serializers.FloriwaySerializer
    filter_fields = ('invoice_number', 'loading_address')