import json
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_signal_format")

# Test signal
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

# Create a simplified _format_signal_message implementation based on bot.py
def format_signal_message(signal_data):
    """Format signal data into a nice message for Telegram (mirroring bot.py logic)"""
    try:
        # Log the signal data
        logger.info(f"[format_signal_message] Received signal_data: {json.dumps(signal_data)}")

        # Extract fields from signal data
        instrument = signal_data.get('instrument', 'Unknown')
        direction = signal_data.get('direction', 'Unknown')
        entry = signal_data.get('entry', 'Unknown')
        stop_loss = signal_data.get('stop_loss')
        take_profit = signal_data.get('take_profit')
        timeframe = signal_data.get('timeframe', '1h')
        tp1 = signal_data.get('tp1', take_profit)
        tp2 = signal_data.get('tp2')
        tp3 = signal_data.get('tp3')
        direction_emoji = "🟢" if direction.upper() == "BUY" else "🔴"
        
        logger.info(f"[format_signal_message] Extracted TPs: tp1='{tp1}', tp2='{tp2}', tp3='{tp3}'")

        # --- Basic message structure --- 
        message = f"<b>🎯 New Trading Signal 🎯</b>\n\n"
        message += f"<b>Instrument:</b> {instrument}\n"
        message += f"<b>Action:</b> {direction.upper()} {direction_emoji}\n\n"
        message += f"<b>Entry Price:</b> {entry}\n"
        if stop_loss:
            message += f"<b>Stop Loss:</b> {stop_loss} 🔴\n"
        if tp1:
            message += f"<b>Take Profit 1:</b> {tp1} 🎯\n"
        if tp2:
            message += f"<b>Take Profit 2:</b> {tp2} 🎯\n"
        if tp3:
            message += f"<b>Take Profit 3:</b> {tp3} 🎯\n"
        message += f"\n{timeframe}\n"
        message += f"{signal_data.get('strategy', 'TradingView Signal')}\n\n"
        message += "————————————————————\n\n"
        message += "• Position size: 1-2% max\n"
        message += "• Use proper stop loss\n"
        message += "• Follow your trading plan\n\n"
        message += "————————————————————\n\n"
        message += "<b>🤖 SigmaPips AI Verdict:</b>\n\n"

        # --- Construct AI Verdict --- 
        # Directly add the sentiment_verdict if it exists, with an appropriate emoji.
        sentiment_verdict = signal_data.get('sentiment_verdict')
        verdict_emoji = ""
        if sentiment_verdict:
            logger.info(f"[format_signal_message] Adding sentiment verdict: {sentiment_verdict}")
            if "aligns" in sentiment_verdict.lower():
                verdict_emoji = "✅ "
            elif "does not align" in sentiment_verdict.lower() or "contradicts" in sentiment_verdict.lower():
                verdict_emoji = "❌ "
            # Add other conditions for neutral etc. if needed, otherwise no emoji
            
            message += f"{verdict_emoji}{sentiment_verdict}"
        else:
            logger.warning("[format_signal_message] No sentiment_verdict found in signal_data.")
            message += "AI analysis could not be completed." # Fallback message

        return message
        
    except Exception as e:
        logger.error(f"Error formatting signal message: {str(e)}")
        # Return simple message on error
        return f"New {signal_data.get('instrument', 'Unknown')} {signal_data.get('direction', 'Unknown')} Signal"

if __name__ == "__main__":
    # Test the message formatter
    formatted_message = format_signal_message(test_signal)
    print("\n\nFORMATTED MESSAGE OUTPUT:")
    print("=======================")
    print(formatted_message)
    print("=======================") 