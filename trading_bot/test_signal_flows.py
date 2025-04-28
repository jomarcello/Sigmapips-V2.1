#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("signal_flow_test")

# Import necessary modules
from telegram import Update, CallbackQuery, User, Message, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# Import our service
from trading_bot.services.telegram_service.bot import TelegramService
from trading_bot.services.database.db import Database

class MockQuery:
    """Mock class for callback query testing"""
    def __init__(self, data, message):
        self.data = data
        self.message = message
        self.id = "test123"
    
    async def answer(self, *args, **kwargs):
        logger.info(f"Mock query answered: {self.data}")
        return True
    
    async def edit_message_text(self, text, **kwargs):
        logger.info(f"Mock edit_message_text: {text[:30]}...")
        return True
    
    async def edit_message_media(self, media, **kwargs):
        logger.info(f"Mock edit_message_media called")
        return True
    
    async def edit_message_caption(self, caption, **kwargs):
        logger.info(f"Mock edit_message_caption: {caption[:30]}...")
        return True

class MockMessage:
    """Mock class for message testing"""
    def __init__(self, message_id=1, chat_id=123456):
        self.message_id = message_id
        self.chat_id = chat_id
    
    async def delete(self):
        logger.info(f"Mock message deleted")
        return True
    
    async def reply_text(self, text, **kwargs):
        logger.info(f"Mock reply_text: {text[:30]}...")
        return True

class MockUser:
    """Mock class for user testing"""
    def __init__(self, id=123456, username="test_user"):
        self.id = id
        self.username = username

class MockChat:
    """Mock class for chat testing"""
    def __init__(self, id=123456):
        self.id = id

class MockBot:
    """Mock class for bot testing"""
    async def send_message(self, chat_id, text, **kwargs):
        logger.info(f"Mock send_message to {chat_id}: {text[:30]}...")
        return MockMessage()
    
    async def send_photo(self, chat_id, photo, **kwargs):
        logger.info(f"Mock send_photo to {chat_id}")
        return MockMessage()
    
    async def edit_message_text(self, chat_id, message_id, text, **kwargs):
        logger.info(f"Mock edit_message_text to {chat_id}: {text[:30]}...")
        return True

class MockContext:
    """Mock class for context testing"""
    def __init__(self):
        self.user_data = {
            'from_signal': True,
            'instrument': 'EURUSD',
            'signal_instrument': 'EURUSD',
            'signal_id': 'EURUSD_BUY_1h_99999',
            'signal_instrument_backup': 'EURUSD',
            'signal_id_backup': 'EURUSD_BUY_1h_99999',
            'signal_direction_backup': 'BUY',
            'signal_timeframe_backup': '1h',
            'is_signals_context': True,
            'signal_direction': 'BUY',
            'signal_timeframe': '1h',
            'original_signal_message': '🎯 New Trading Signal 🎯\n\nInstrument: EURUSD\nAction: BUY 🟢\n\nEntry Price: 1.0850\nStop Loss: 1.0800 🔴\nTake Profit 1: 1.0900 🎯\nTake Profit 2: 1.0950 🎯\nTake Profit 3: 1.1000 🎯\n\n1h\nTradingView Signal\n\n————————————————————\n\n• Position size: 1-2% max\n• Use proper stop loss\n• Follow your trading plan\n\n————————————————————\n\n🤖 SigmaPips AI Verdict:\n\nThe EURUSD buy signal shows a promising setup with defined entry at 1.0850 and stop loss at 1.0800. Trade aligns with market sentiment. Multiple take profit levels provide opportunities for partial profit taking. The risk-reward ratio is reasonable at 1.00:1.',
            'analysis_type': 'technical'
        }
        self.bot = MockBot()

async def test_signal_technical():
    """Test signal_technical_callback and show_technical_analysis"""
    # Create database connection (use mock or test DB)
    db = Database(connection_string="sqlite:///:memory:")
    
    # Create service instance
    service = TelegramService(db=db, lazy_init=True)
    
    # Create mock objects
    mock_chat = MockChat()
    mock_user = MockUser()
    mock_message = MockMessage()
    mock_query = MockQuery(data="signal_technical", message=mock_message)
    
    # Create mock update
    update = Update._get_empty_object()
    update._effective_chat = mock_chat
    update._effective_user = mock_user
    update._callback_query = mock_query
    
    # Create mock context
    context = MockContext()
    
    # Test signal_technical_callback
    logger.info("Testing signal_technical_callback...")
    try:
        result = await service.signal_technical_callback(update, context)
        logger.info(f"signal_technical_callback result: {result}")
    except Exception as e:
        logger.error(f"Error in signal_technical_callback: {str(e)}")
        raise

async def test_signal_sentiment():
    """Test signal_sentiment_callback and show_sentiment_analysis"""
    # Create database connection (use mock or test DB)
    db = Database(connection_string="sqlite:///:memory:")
    
    # Create service instance
    service = TelegramService(db=db, lazy_init=True)
    
    # Create mock objects
    mock_chat = MockChat()
    mock_user = MockUser()
    mock_message = MockMessage()
    mock_query = MockQuery(data="signal_sentiment", message=mock_message)
    
    # Create mock update
    update = Update._get_empty_object()
    update._effective_chat = mock_chat
    update._effective_user = mock_user
    update._callback_query = mock_query
    
    # Create mock context
    context = MockContext()
    
    # Test signal_sentiment_callback
    logger.info("Testing signal_sentiment_callback...")
    try:
        result = await service.signal_sentiment_callback(update, context)
        logger.info(f"signal_sentiment_callback result: {result}")
    except Exception as e:
        logger.error(f"Error in signal_sentiment_callback: {str(e)}")
        raise

async def test_signal_calendar():
    """Test signal_calendar_callback and show_economic_calendar"""
    # Create database connection (use mock or test DB)
    db = Database(connection_string="sqlite:///:memory:")
    
    # Create service instance
    service = TelegramService(db=db, lazy_init=True)
    
    # Create mock objects
    mock_chat = MockChat()
    mock_user = MockUser()
    mock_message = MockMessage()
    mock_query = MockQuery(data="signal_calendar", message=mock_message)
    
    # Create mock update
    update = Update._get_empty_object()
    update._effective_chat = mock_chat
    update._effective_user = mock_user
    update._callback_query = mock_query
    
    # Create mock context
    context = MockContext()
    
    # Test signal_calendar_callback
    logger.info("Testing signal_calendar_callback...")
    try:
        result = await service.signal_calendar_callback(update, context)
        logger.info(f"signal_calendar_callback result: {result}")
    except Exception as e:
        logger.error(f"Error in signal_calendar_callback: {str(e)}")
        raise

async def main():
    """Run all tests"""
    logger.info("Starting signal flow tests...")
    
    # Test each flow
    await test_signal_technical()
    await test_signal_sentiment()
    await test_signal_calendar()
    
    logger.info("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 