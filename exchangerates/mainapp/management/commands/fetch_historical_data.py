from django.core.management.base import BaseCommand
from mainapp.models import ExchangeRate 
from mainapp.exchange_data import fetch_historical_data 
from datetime import date, datetime
from mainapp.api_config import api_url, params 


class Command(BaseCommand):
    help = "Populate the database with historical exchange rate data."

    def add_arguments(self, parser):
        parser.add_argument("start_date", help="Start date for historical data (YYYY-MM-DD)")
        parser.add_argument("end_date", help="End date for historical data (YYYY-MM-DD)")

    def handle(self, *args, **options):
        start_date_str = options["start_date"]
        end_date_str = options["end_date"]

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d") 
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Error parsing dates: {e}"))
            return
        
        historical_data = fetch_historical_data(api_url, params, start_date, end_date)

        if historical_data:
            for data in historical_data:
                ExchangeRate.objects.create(
                    upload_date = date.today(), 
                    exchange_date = data["date"],
                    base_currency = data["base"],
                    usd_rate = data["rates"]["USD"],
                    gbp_rate = data["rates"]["GBP"],
                    ron_rate = data["rates"]["RON"]
                )

            self.stdout.write(self.style.SUCCESS("Historical data populated successfully."))

        else:
            self.stdout.write(self.style.ERROR("Failed to retrieve historical data."))