from django.db import models

class ExchangeRate(models.Model):
    upload_date = models.DateField()
    exchange_date = models.DateField(primary_key=True)
    base_currency = models.CharField(max_length=3)
    usd_rate = models.FloatField()
    gbp_rate = models.FloatField()
    ron_rate = models.FloatField()

    class Meta:
        db_table = "exchange_rates"