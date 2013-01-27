from django.core.management.base import BaseCommand
from datetime import datetime 
from icarus.models import Site
from _update_weather import update_weather
from _delete_weather import delete_weather

class Command(BaseCommand):
    args = 'No args'
    help = 'Deletes and then pulls new weather information for all sites'

    def handle(self, *args, **options):
        site_list = Site.objects.all()
        for site in site_list:
            self.stdout.write("Updating Predictions for %s" % site)
            self.stdout.write("Deleting previous Predictions")
            delete_weather(site)
            self.stdout.write("Getting new Weather Predictions")
            update_weather(site)
            site.last_weather_refresh = datetime.now()
            site.save()
