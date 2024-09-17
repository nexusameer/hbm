from rest_framework import serializers
from . import models

class FloriwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floriway
        fields = '__all__'
