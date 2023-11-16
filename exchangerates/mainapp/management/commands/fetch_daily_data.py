from django.core.management.base import BaseCommand
from mainapp.models import ExchangeRate 
from mainapp.exchange_data import fetch_daily_data
from datetime import datetime, date
from mainapp.api_config import api_url, params


class Command(BaseCommand):
    help = "Fetch and update the database with daily exchange rate data."

    def handle(self, *args, **options):

        last_data = ExchangeRate.objects.order_by("-exchange_date").first()
        last_date = last_data.exchange_date if last_data else datetime.now()

        data = fetch_daily_data(api_url, params, last_date)

        if data:
            exchange_date = datetime.strptime(data["date"], "%Y-%m-%d")

            existing_data = ExchangeRate.objects.filter(exchange_date=exchange_date).first()

            if not existing_data:
                ExchangeRate.objects.create(
                    upload_date = date.today(), 
                    exchange_date = data["date"],
                    base_currency = data["base"],
                    usd_rate = data["rates"]["USD"],
                    gbp_rate = data["rates"]["GBP"],
                    ron_rate = data["rates"]["RON"]
                )

                self.stdout.write(self.style.SUCCESS("Daily data fetched and updated successfully."))
            else:
                self.stdout.write(self.style.SUCCESS("Daily data already exists in the database."))
        else:
            self.stdout.write(self.style.ERROR("Failed to retrieve daily data."))
