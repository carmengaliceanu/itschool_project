from django.shortcuts import render, HttpResponse
from django.core.exceptions import ValidationError
from mainapp.models import ExchangeRate
from mainapp.forms import DateRangeForm, ExchangeCalculatorForm
import csv
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd


def home(request):
    return render(request, "mainapp/home.html")


def download_csv(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)

        try:
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]

                queryset = ExchangeRate.objects.filter(exchange_date__range=(start_date, end_date))

                if not queryset.exists():
                    raise ValidationError("No data available for the selected timeframe.")
                
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = f"attachment; filename='exchange_rates_{start_date}_{end_date}.csv'"

                writer = csv.writer(response)
                writer.writerow(["Date", "Base Currency", "USD Rate", "GBP Rate", "RON Rate"])

                for data in queryset:
                    writer.writerow([data.exchange_date,
                                    data.base_currency, 
                                    round(data.usd_rate,2),
                                    round(data.gbp_rate,2), 
                                    round(data.ron_rate,2)])

                return response
            
        except ValidationError as e:
            error_message = e.message if isinstance(e.message, str) else str(e.message[0])
            form.add_error(None, error_message)

    else:
        form = DateRangeForm()

    return render(request, "mainapp/download_csv.html", {"form": form})


def exchange_calculator(request):
    if request.method == "POST":
        form = ExchangeCalculatorForm(request.POST)

        current_date = datetime.now().strftime("%Y-%m-%d")

        if form.is_valid():
            amount_in_eur = form.cleaned_data["amount_in_eur"]

            latest_exchange_rates = ExchangeRate.objects.filter(exchange_date=datetime.now()).values("usd_rate", "gbp_rate", "ron_rate").first()
            
            if latest_exchange_rates:
                amount_in_usd = amount_in_eur * latest_exchange_rates["usd_rate"]
                amount_in_gbp = amount_in_eur * latest_exchange_rates["gbp_rate"]
                amount_in_ron = amount_in_eur * latest_exchange_rates["ron_rate"]

                return render(request, "mainapp/exchange_calculator_result.html", {
                            "form": form,
                            "amount_in_eur": round(amount_in_eur,2),
                            "amount_in_usd": round(amount_in_usd,2),
                            "amount_in_gbp": round(amount_in_gbp,2),                                 
                            "amount_in_ron": round(amount_in_ron,2),
                            "current_date": current_date
                            })                                                                                                                      
            
            form.add_error(None, "No exchange rates available for the current day.")

    else:
        form = ExchangeCalculatorForm()

    return render(request, "mainapp/exchange_calculator.html", {"form": form})


def exchange_line_chart(request):
    exchange_data = ExchangeRate.objects.all()

    df = pd.DataFrame.from_records(exchange_data.values())

    df["exchange_date"] = pd.to_datetime(df["exchange_date"])
    df = df.sort_values(by="exchange_date")

    df["usd_rate"] = df["usd_rate"].round(2)
    df["gbp_rate"] = df["gbp_rate"].round(2)
    df["ron_rate"] = df["ron_rate"].round(2)

    #Create scatter plots
    fig_usd = go.Figure()
    fig_usd.add_trace(go.Scatter(x=df["exchange_date"], y=df["usd_rate"], mode="lines", name="USD Rate", marker=dict(color="darkorange")))
    fig_usd.update_layout(title="USD Rate Line Chart", xaxis=dict(tickmode="linear", dtick="M1"))

    fig_gbp = go.Figure()
    fig_gbp.add_trace(go.Scatter(x=df["exchange_date"], y=df["gbp_rate"], mode="lines", name="GBP Rate", marker=dict(color="darkturquoise")))
    fig_gbp.update_layout(title="GBP Rate Line Chart", xaxis=dict(tickmode="linear", dtick="M1"))

    fig_ron = go.Figure()
    fig_ron.add_trace(go.Scatter(x=df["exchange_date"], y=df["ron_rate"], mode="lines", name="RON Rate", marker=dict(color="darkgrey")))
    fig_ron.update_layout(title="RON Rate Line Chart", xaxis=dict(tickmode="linear", dtick="M1")) 

    #Convert the Plotly figures to HTML
    chart_html_usd = fig_usd.to_html(full_html=False)
    chart_html_gbp = fig_gbp.to_html(full_html=False)
    chart_html_ron = fig_ron.to_html(full_html=False)

    return render(request, "mainapp/exchange_line_chart.html", {
        "chart_html_usd": chart_html_usd,
        "chart_html_gbp": chart_html_gbp,
        "chart_html_ron": chart_html_ron,
    })