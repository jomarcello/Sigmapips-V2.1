#!/usr/bin/env python3
import requests
import json
import time

# De Railway URL van je applicatie
RAILWAY_URL = "https://sigmapips-v2-production.up.railway.app"
SIGNAL_ENDPOINT = f"{RAILWAY_URL}/signal"

# Test signaal data
signal_data = {
    "instrument": "EURUSD",
    "direction": "BUY",
    "entry": "1.12345",
    "stop_loss": "1.12000",
    "take_profit": "1.13000",
    "tp1": "1.12800",
    "tp2": "1.13200",
    "tp3": "1.13600",
    "timeframe": "1h",
    "strategy": "Test Signal naar Railway"
}

print(f"Versturen van test signaal naar: {SIGNAL_ENDPOINT}")
print(f"Data: {json.dumps(signal_data, indent=2)}")

try:
    # Verstuur het signaal naar het /signal endpoint
    response = requests.post(
        SIGNAL_ENDPOINT, 
        data=json.dumps(signal_data),
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Signaal succesvol verstuurd! Controleer je Telegram bot voor het bericht.")
    else:
        print("\n❌ Er is iets misgegaan bij het versturen van het signaal.")
        
except Exception as e:
    print(f"Error bij het versturen van het signaal: {e}")

# Wacht even zodat de gebruiker de output kan lezen
time.sleep(1) 