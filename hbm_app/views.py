# from django.shortcuts import render

from django.http.response import JsonResponse
from django.views.generic.base import TemplateView
from . import models
from . import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.decorators import login_required
from django.core.management import call_command

class CustomerViewSet(ReadOnlyModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filter_fields = ('name',)

class TransactionViewSet(ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    filter_fields = ('customer',)

class AhWeekTransactionViewSet(ReadOnlyModelViewSet):
    queryset = models.AhWeekTransaction.objects.all()
    serializer_class = serializers.AhWeekTransactionSerializer
    filterset_fields = {
        'article': ['exact', 'in'],
        'week': ['gte', 'lte', 'exact', 'in'],
        'year': ['gte', 'lte', 'exact', 'in']
    }


class AhDayTransactionViewSet(ReadOnlyModelViewSet):
    queryset = models.AhDayTransaction.objects.all()
    serializer_class = serializers.AhDayTransactionSerializer

class AhPeriodTransactionViewSet(ReadOnlyModelViewSet):
    queryset = models.AhPeriodTransaction.objects.all()
    serializer_class = serializers.AhPeriodTransactionSerializer

class TransactionTestViewSet(ReadOnlyModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    pagination_class = None
    filterset_fields = {
        'customer': ['exact'],
        'date': ['gte', 'gt', 'lt', 'lte', 'exact']
    }

class ActionLogViewSet(ReadOnlyModelViewSet):
    queryset = models.ActionLog.objects.all()
    serializer_class = serializers.ActionLogSerializer
    filter_fields = ('completed',)

class ErrorLogViewSet(ReadOnlyModelViewSet):
    queryset = models.ErrorLog.objects.all()
    serializer_class = serializers.ErrorLogSerializer

class ScheduleViewSet(ReadOnlyModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer

class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer

class ArticleTypeViewSet(ReadOnlyModelViewSet):
    queryset = models.ArticleType.objects.all()
    serializer_class = serializers.ArticleTypeSerializer

class EventViewSet(ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

class DatedEventViewSet(ReadOnlyModelViewSet):
    queryset = models.DatedEvent.objects.all()
    serializer_class = serializers.DatedEventSerializer

class AgreflorViewSet(ReadOnlyModelViewSet):
    queryset = models.Agreflor.objects.all()
    serializer_class = serializers.AgreflorSerializer

class AntennaViewSet(ReadOnlyModelViewSet):
    queryset = models.Antenna.objects.all()
    serializer_class = serializers.AntennaSerializer

class WematransViewSet(ReadOnlyModelViewSet):
    queryset = models.Wematrans.objects.all()
    serializer_class = serializers.WematransSerializer

class CustomCommandView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/login/'
    template_name = 'custom_commands.html'

    def get(self, request, *args, **kwargs):
        all_commands = models.CustomCommand.objects.all()
        return render(request, self.template_name,
                      {'commands': all_commands})


@login_required
def execute_command(request, pk):
    command = models.CustomCommand.objects.get(id=pk)
    data = dict()
    try:
        call_command(command.command)
        data['executed'] = True
    except:
        data['executed'] = False
    return JsonResponse(data)
