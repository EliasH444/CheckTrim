Automated Appointment Availability Checker

A Python tool that monitors appointment availability for any service and sends instant notifications via Telegram. Built with automation, API integration, and reverse-engineering techniques.

Project Overview

Booking appointments can be frustrating with constantly changing availability. I built this project to monitor slots for my barber at Barberhood, ensuring I never miss a booking.

Initial attempts: Tried browser automation (Selenium), which was slow, error-prone, and unreliable.
Final solution: Reverse-engineered the Barberhood API by inspecting network requests in the browser. This allows direct and reliable API calls.
Monitors available slots, filters unavailable days, and sends instant Telegram notifications.

⚠️ While this project demonstrates the solution for a personal barber at Barberhood, the repository uses generic placeholders for privacy. If someone wanted to apply this to their barber, they would need to inspect network requests themselves to find the proper service and provider IDs.

Key Features
Feature	Benefit
Direct API calls via reverse-engineered endpoints	Reliable and fast, avoids fragile web scraping
Telegram notifications	Instant updates for newly available slots
Dynamic configuration reload	Change target service or monitoring interval without restarting
Closed day filtering	Automatically skips days when the service is unavailable
Extensible	Can monitor multiple services or providers in a single run
How It Works
Reads settings from a config.ini file.
Calls the API (discovered via network inspection) to fetch unavailable dates.
Computes available dates for the next N days, skipping closed days.
Sends Telegram notifications for newly available slots.
Runs repeatedly every X minutes (configurable).
Installation & Usage

Clone the repository:

git clone https://github.com/<your-username>/appointment-checker.git
cd appointment-checker
pip install requests

Edit config.ini with your bot credentials and service details:

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

Run the checker:

python checker.py

To adapt this to your own barber or service, you would need to inspect network requests in your browser while using the booking site to find the service ID, provider ID, and location ID.