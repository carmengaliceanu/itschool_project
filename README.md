Overview:
This project, built with Django, interacts with the http://api.exchangeratesapi.io/v1/ to fetch and manage currency exchange rate data. 

Features:
Fetch Historical Data: Use the fetch_historical_data command to retrieve historical exchange rate data.
Fetch Daily Data: Use the fetch_daily_data command to get the latest daily exchange rates.

Data Storage:
Exchange rate data is stored in a SQLite database. The database schema and structure are defined in mainapp/models.py.

Web App:
The project includes a web application that allows users to interact with the stored exchange rate data. 
Users can perform various actions: exchange calculator, download CSV, view Chart.

Web Application:
Run the development server.
Access the web app at http://localhost:8000.
