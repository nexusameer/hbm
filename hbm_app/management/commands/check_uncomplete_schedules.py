from django.core.management.base import BaseCommand
import hbm_app.python_scripts.run_script as run_script

class Command(BaseCommand):
    help = 'Check uncomplete schedules'

    def handle(self, *args, **kwargs):
        run_script.run_function("check_uncomplete_schedules")