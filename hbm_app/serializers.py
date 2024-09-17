from rest_framework import serializers
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'

class AhWeekTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AhWeekTransaction
        fields = '__all__'

class AhDayTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AhDayTransaction
        fields = '__all__'

class AhPeriodTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AhPeriodTransaction
        fields = '__all__'

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActionLog
        fields = '__all__'

class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ErrorLog
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'

class ArticleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class DatedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatedEvent
        fields = '__all__'

class AgreflorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agreflor
        fields = '__all__'

class AntennaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Antenna
        fields = '__all__'

class WematransSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wematrans
        fields = '__all__'