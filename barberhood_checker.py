#!/usr/bin/env python3
"""
Barberhood Availability Checker
================================
Calls the Barberhood API directly to find available dates for a barber,
then notifies via Telegram.

All settings are in config.ini — no need to edit this file!

Requirements:
    pip install requests

Usage:
    python barberhood_checker.py
"""

import time
import configparser
import requests
from datetime import datetime, timedelta

# ── Load config ───────────────────────────────────────────
config = configparser.ConfigParser()
config.read("config.ini")

TELEGRAM_BOT_TOKEN     = config["TELEGRAM"]["bot_token"]
TELEGRAM_CHAT_ID       = config["TELEGRAM"]["chat_id"]
BOOKING_URL            = config["BOOKING"]["url"]
TARGET_BARBER          = config["BOOKING"]["barber"].strip()
TARGET_SERVICE         = config["BOOKING"]["service"].strip()
SERVICE_ID             = config["BOOKING"]["service_id"].strip()
PROVIDER_ID            = config["BOOKING"]["provider_id"].strip()
LOC_ID                 = config["BOOKING"]["loc_id"].strip()
DAYS_AHEAD             = int(config["BOOKING"]["days_ahead"])
CHECK_INTERVAL_MINUTES = int(config["CHECKER"]["interval_minutes"])

API_URL = "https://www.thebarberhood.co.uk/appointments/ajax_get_unavailable_dates_MULTI"

HEADERS = {
    "User-Agent":        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With":  "XMLHttpRequest",
    "Origin":            "https://www.thebarberhood.co.uk",
    "Referer":           "https://www.thebarberhood.co.uk/book",
}

# Days the shop is closed (0=Monday, 6=Sunday)
CLOSED_DAYS = {0, 6}  # Monday and Sunday
# ─────────────────────────────────────────────────────────


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_telegram(message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print(f"[{now()}] ✅ Telegram notification sent.")
    except Exception as e:
        print(f"[{now()}] ❌ Telegram error: {e}")


def get_unavailable_dates(service_id: str, provider_id: str, loc_id: str) -> set:
    """Call the Barberhood API and return a set of unavailable date strings."""
    data = {
        "no_services":   "1",
        "selected_date": datetime.today().strftime("%Y-%m-%d"),
        "loc_id":        loc_id,
        "service_id1":   service_id,
        "provider_id1":  provider_id,
    }
    try:
        r = requests.post(API_URL, data=data, headers=HEADERS, timeout=15)
        r.raise_for_status()
        response = r.json()
        print(f"[{now()}] 📡 Raw API response: {response}")

        # Handle both array and object responses
        if isinstance(response, list):
            return set(response)
        elif isinstance(response, dict):
            # Try common key names
            for key in ("dates", "unavailable", "unavailable_dates", "data"):
                if key in response:
                    return set(response[key])
            # If no known key, collect all string values that look like dates
            dates = set()
            for v in response.values():
                if isinstance(v, list):
                    dates.update(v)
            return dates
    except Exception as e:
        print(f"[{now()}] ❌ API error: {e}")
    return set()


def check_availability(service_id: str, provider_id: str, loc_id: str) -> list:
    """Return a sorted list of available date strings."""
    unavailable = get_unavailable_dates(service_id, provider_id, loc_id)

    available = []
    for i in range(DAYS_AHEAD):
        date = datetime.today().date() + timedelta(days=i)
        if date.weekday() in CLOSED_DAYS:
            continue
        date_str = date.strftime("%Y-%m-%d")
        if date_str not in unavailable:
            available.append(date_str)

    print(f"[{now()}] 📅 Unavailable: {sorted(unavailable)}")
    print(f"[{now()}] ✅ Available  : {available}")
    return available


def reload_config():
    """Re-read config.ini so changes apply without restarting."""
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    return (
        cfg["BOOKING"]["barber"].strip(),
        cfg["BOOKING"]["service"].strip(),
        cfg["BOOKING"]["service_id"].strip(),
        cfg["BOOKING"]["provider_id"].strip(),
        cfg["BOOKING"]["loc_id"].strip(),
        int(cfg["BOOKING"]["days_ahead"]),
        int(cfg["CHECKER"]["interval_minutes"]),
    )


def main():
    barber, service, service_id, provider_id, loc_id, days_ahead, interval = reload_config()

    print("=" * 55)
    print("  🪒  Barberhood Availability Checker")
    print(f"  Barber     : {barber}  (provider_id={provider_id})")
    print(f"  Service    : {service}  (service_id={service_id})")
    print(f"  Days ahead : {days_ahead}")
    print(f"  Interval   : every {interval} minutes")
    print("=" * 55)
    print("  💡 Edit config.ini to change barber/service.")
    print("     Changes apply on the next check automatically!")
    print("=" * 55)

    send_telegram(
        f"🪒 <b>Barberhood Checker Started</b>\n"
        f"Barber: <b>{barber}</b>\n"
        f"Service: {service}\n"
        f"Checking {days_ahead} days ahead, every {interval} minutes.\n\n"
        f"💡 Edit config.ini to change barber anytime."
    )

    last_available = set()
    last_barber = barber

    while True:
        barber, service, service_id, provider_id, loc_id, days_ahead, interval = reload_config()

        # Notify if barber was changed in config.ini
        if barber != last_barber:
            print(f"[{now()}] 🔄 Barber changed: {last_barber} → {barber}")
            send_telegram(
                f"🔄 <b>Barber changed to: {barber}</b>\n"
                f"Now monitoring <b>{barber}</b> for {service}."
            )
            last_barber = barber
            last_available = set()

        print(f"\n[{now()}] 🔍 Checking available dates for {barber}...")
        available = check_availability(service_id, provider_id, loc_id)

        if available:
            available_set = set(available)
            new_dates = available_set - last_available

            if new_dates:
                date_list = "\n".join(f"  • {d}" for d in sorted(new_dates))
                message = (
                    f"🟢 <b>Available dates for {barber}!</b>\n"
                    f"Service: {service}\n\n"
                    f"New available dates:\n{date_list}\n\n"
                    f"👉 Book now: {BOOKING_URL}"
                )
                send_telegram(message)
                print(f"[{now()}] 🎉 New dates available: {sorted(new_dates)}")
            else:
                print(f"[{now()}] ℹ️  No change — available dates: {sorted(available)}")

            last_available = available_set
        else:
            print(f"[{now()}] ❌ No available dates found for {barber} in the next {days_ahead} days.")
            last_available = set()

        print(f"[{now()}] 💤 Sleeping {interval} minutes...\n")
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()