from django.urls import path
from mainapp import views

urlpatterns = [
    path("", views.home, name="home"), 
    path("exchange-calculator/", views.exchange_calculator, name="exchange_calculator"),
    path("download-csv/", views.download_csv, name="download_csv"),   
    path("exchange-chart/", views.exchange_line_chart, name="exchange_line_chart")
]
