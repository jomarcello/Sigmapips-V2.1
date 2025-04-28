import json
import asyncio
import logging
import os
import sys
from pathlib import Path
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("direct_test")

# Test signal message
test_message = """<b>🎯 New Trading Signal 🎯</b>

<b>Instrument:</b> EURUSD
<b>Action:</b> BUY 🟢

<b>Entry Price:</b> 1.0850
<b>Stop Loss:</b> 1.0800 🔴
<b>Take Profit 1:</b> 1.0900 🎯
<b>Take Profit 2:</b> 1.0950 🎯
<b>Take Profit 3:</b> 1.1000 🎯

1h
TradingView Signal

————————————————————

• Position size: 1-2% max
• Use proper stop loss
• Follow your trading plan

————————————————————

<b>🤖 SigmaPips AI Verdict:</b>

The EURUSD buy signal shows a promising setup with defined entry at 1.0850 and stop loss at 1.0800. Trade aligns with market sentiment. Multiple take profit levels provide opportunities for partial profit taking. The risk-reward ratio is reasonable at 1.00:1."""

async def main():
    # Initialize with your bot token
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7328581013:AAGDFJyvipmQsV5UQLjUeLQmX2CWIU2VMjk")
    
    # Your Telegram user ID for testing
    user_id = 2004519703  # Replace with your actual Telegram user ID
    
    # Prepare keyboard with analysis options
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔍 Analyze Market", "callback_data": "analyze_from_signal_EURUSD_EURUSD_BUY_1h_99999"}]
        ]
    }
    
    try:
        # Send the test message
        logger.info(f"Sending test message to user ID: {user_id}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": user_id,
                    "text": test_message,
                    "parse_mode": "HTML",
                    "reply_markup": keyboard
                }
            )
            
            if response.status_code == 200:
                logger.info("Message sent successfully!")
                logger.info(f"Response: {response.json()}")
            else:
                logger.error(f"Error sending message: {response.status_code}")
                logger.error(f"Response: {response.text}")
                
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 