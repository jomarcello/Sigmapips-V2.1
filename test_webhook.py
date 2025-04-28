#!/usr/bin/env python3
import requests
import json
import os
import sys

def send_test_signal(webhook_url=None):
    """
    Stuur een test trading signaal naar de webhook URL.
    Als geen URL is opgegeven, wordt geprobeerd deze uit de omgevingsvariabelen te halen.
    """
    if not webhook_url:
        # Probeer de webhook URL uit environment variabelen te halen
        base_url = os.getenv("WEBHOOK_URL", "")
        webhook_path = os.getenv("WEBHOOK_PATH", "/webhook")
        
        # Controleer of de base URL is ingesteld
        if not base_url:
            print("ERROR: Geen webhook URL opgegeven en WEBHOOK_URL environment variabele niet gevonden.")
            print("Gebruik: python test_webhook.py [webhook_url]")
            sys.exit(1)
            
        # Zorg ervoor dat base_url geen slash op het einde heeft
        if base_url.endswith("/"):
            base_url = base_url[:-1]
            
        # Zorg ervoor dat webhook_path met een slash begint
        if not webhook_path.startswith("/"):
            webhook_path = "/" + webhook_path
            
        # Maak de volledige URL
        webhook_url = f"{base_url}{webhook_path}"
    
    print(f"Versturen van test signaal naar: {webhook_url}")
    
    # Voorbeeld test signaal data
    signal_data = {
        "instrument": "EURUSD",
        "direction": "BUY",
        "entry": "1.12345",
        "stop_loss": "1.12000",
        "take_profit": "1.13000",
        "timeframe": "1h",
        "strategy": "Test Signal van Python Script"
    }
    
    # Een alternatief endpoint voor signalen is /signal
    signal_url = webhook_url.replace("/webhook", "/signal")
    print(f"Versturen naar signal endpoint: {signal_url}")
    
    try:
        # Verstuur het signaal naar het /signal endpoint
        response = requests.post(
            signal_url, 
            data=json.dumps(signal_data),
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")
        
        return True
    except Exception as e:
        print(f"Error bij het versturen van het signaal: {e}")
        return False

if __name__ == "__main__":
    # Controleer of een webhook URL is opgegeven als command line argument
    if len(sys.argv) > 1:
        webhook_url = sys.argv[1]
        send_test_signal(webhook_url)
    else:
        # Geen URL opgegeven, probeer uit environment variabelen te halen
        send_test_signal() 