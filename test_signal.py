import json
import asyncio
import logging
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from trading_bot.services.database.db import Database
from trading_bot.services.telegram_service.bot import TelegramService

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_signal")

# Create a test signal
test_signal = {
    "instrument": "EURUSD",
    "direction": "BUY",
    "entry": "1.0850",
    "stop_loss": "1.0800",
    "take_profit": "1.0900",
    "tp1": "1.0900",
    "tp2": "1.0950",
    "tp3": "1.1000",
    "timeframe": "1h",
    "sentiment_verdict": "Trade aligns with market sentiment."
}

async def main():
    # Initialize database
    logger.info("Initializing database...")
    db = Database(
        supabase_url=os.environ.get("SUPABASE_URL", "https://utigkgjcyqnrhpndzqhs.supabase.co"),
        supabase_key=os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0aWdrZ2pjeXFucmhwbmR6cWhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODYwODIwMTksImV4cCI6MjAwMTY1ODAxOX0.OenKCdDFUHA5vPsEH9LbNQvJrkedHXV2SffNEcUPBn8")
    )
    
    # Initialize telegram service directly with lazy loading
    logger.info("Initializing Telegram service (lazy init)...")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7328581013:AAGDFJyvipmQsV5UQLjUeLQmX2CWIU2VMjk")
    # Pass lazy_init=True to prevent chart service loading
    telegram_service = TelegramService(db=db, bot_token=bot_token, lazy_init=True) 
    
    # Add your Telegram user ID here for testing
    logger.info("Setting admin users...")
    telegram_service.admin_users = [2004519703]  # Replace with your Telegram user ID
    
    # Process test signal (includes sentiment_verdict)
    logger.info(f"Processing test signal: {test_signal}")
    success = await telegram_service.process_signal(test_signal)
    
    if success:
        logger.info("Test signal processed successfully!")
    else:
        logger.error("Failed to process test signal")
    
    # Wait a bit before exiting
    await asyncio.sleep(3)
    logger.info("Test completed")

if __name__ == "__main__":
    asyncio.run(main()) 