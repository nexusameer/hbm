from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'test', views.TransactionTestViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'ah-day-transactions', views.AhDayTransactionViewSet)
router.register(r'ah-week-transactions', views.AhWeekTransactionViewSet)
router.register(r'ah-period-transactions', views.AhPeriodTransactionViewSet)
router.register(r'actionlog', views.ActionLogViewSet)
router.register(r'errorlog', views.ErrorLogViewSet)
router.register(r'Schedule', views.ScheduleViewSet)
router.register(r'Article', views.ArticleViewSet)
router.register(r'Agreflor', views.AgreflorViewSet)
router.register(r'Antenna', views.AntennaViewSet)
router.register(r'Wematrans', views.WematransViewSet)
router.register(r'article-type', views.ArticleTypeViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'dated-event', views.DatedEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('custom_commands', views.CustomCommandView.as_view(), name="custom_commands"),
    path('execute_command/<int:pk>', views.execute_command, name="execute_command")
]