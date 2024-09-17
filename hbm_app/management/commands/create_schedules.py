from django.core.management.base import BaseCommand
from hbm_app.python_scripts.schedules import create_schedule

class Command(BaseCommand):
    help = 'Create schedules'

    def handle(self, *args, **kwargs):
        create_schedule()