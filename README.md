🗓️ Automated Appointment Availability Checker

A Python tool that monitors appointment availability for services and sends instant notifications via Telegram. Built using automation, API integration, and reverse-engineering techniques.

🚀 Project Overview

Booking appointments can be frustrating when slots fill up quickly. This project automatically monitors booking slots and alerts you as soon as a slot becomes available.

Originally built for a barber at Barberhood, this solution is generic and can be adapted to other booking services.

🔍 How the solution evolved
Initial approach: Browser automation using Selenium
Slow, fragile, prone to breaking with UI changes
Final approach: Reverse-engineered API calls via browser network inspection
Fast, reliable, scalable, and avoids fragile web scraping
⚠️ Important Note

This repository uses generic placeholders for privacy.
To adapt this tool for your own service:

Open your browser DevTools
Inspect network requests while using the booking site
Identify the required IDs:
service_id
provider_id
location_id
API endpoint URL
✨ Key Features
Feature	Benefit
Direct API integration	Fast and reliable, no scraping
Telegram notifications	Instant alerts for new slots
Dynamic configuration	Change settings without restarting
Closed-day filtering	Automatically skips unavailable days
Extensible	Monitor multiple services/providers simultaneously
⚙️ How It Works
Reads configuration from config.ini
Calls the booking API to fetch unavailable dates
Computes available slots for the next N days
Filters out closed/unavailable days
Sends Telegram notifications for newly available slots
Runs repeatedly at configurable intervals
🛠 Installation & Setup
1. Clone the repository
git clone https://github.com/<your-username>/appointment-checker.git
cd appointment-checker
2. Install dependencies
pip install requests
3. Configure your settings

Edit the config.ini file:

[TELEGRAM]
bot_token = YOUR_BOT_TOKEN
chat_id   = YOUR_CHAT_ID

[BOOKING]
url         = https://example.com/book
service     = Target Service
service_id  = 123
provider_id = 456
location_id = 789
days_ahead  = 14

[CHECKER]
interval_minutes = 10
▶️ Usage

Run the checker:

python checker.py

It will continuously monitor availability and send Telegram alerts when new slots appear.

🔄 Customization Guide

To adapt this tool for another service:

Open the booking website
Open Developer Tools (F12)
Go to the Network tab
Perform a booking search
Locate the API request fetching availability
Extract:
Endpoint URL
Service ID
Provider ID
Location ID
🧠 Technical Highlights
Reverse-engineered API integration
Lightweight polling-based monitoring system
Config-driven design (no hardcoding)
Fast and reliable compared to Selenium/browser automation
📈 Potential Improvements
Multi-service monitoring dashboard
Web UI for configuration
Historical availability tracking with a database
Docker container support
Cloud deployment (AWS EC2 / VPS + cron jobs)
