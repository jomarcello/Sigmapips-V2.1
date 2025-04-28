import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from trading_bot.services.telegram_service import TelegramService
    print("Successfully imported TelegramService")
except Exception as e:
    print(f"Error importing TelegramService: {e}")
    import traceback
    traceback.print_exc() 