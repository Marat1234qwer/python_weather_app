## Application Description

This web application is designed to receive up-to-date weather data.
Main functions:
Requests data via the OpenWeatherMap API (https://api.openweathermap.org/data/2.5/weather).
Hosted on the website https://propogoda.ru.
Developed in Python using the Flask framework.
Automatically updates information every hour.

## Installation and launch instructions:

# Updating packages
apt update && apt upgrade -y
# Installing Python and dependencies
apt install python3 python3-pip python3-venv -y
# Installing Nginx and tools
apt install nginx -y
# Clone the repository or download the files
git clone https://github.com/Marat1234qwer/web_app_weather /var/www
cd /var/www/web_app_weather
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Launching
python3 server.ru

After launching, the application will be available at the server IP address (for example, http://your_IP:5000).