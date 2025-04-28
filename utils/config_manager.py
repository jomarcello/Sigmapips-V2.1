"""
Configuration Manager for the Trading Bot.
Responsible for loading and providing access to configuration values.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration settings for the trading bot."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the config manager.
        
        Args:
            config_path: Optional path to config file. If None, uses default location.
        """
        self._config_path = config_path or os.environ.get('CONFIG_PATH', 'config.json')
        self._config: Dict[str, Any] = {}
        self._load_config()
        
    def _load_config(self):
        """Load configuration from the config file."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r') as f:
                    self._config = json.load(f)
                logger.info(f"Loaded configuration from {self._config_path}")
            else:
                logger.warning(f"Config file {self._config_path} not found. Using environment variables.")
                self._config = {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._config = {}
    
    @property
    def TELEGRAM_BOT_TOKEN(self) -> str:
        """Get the Telegram bot token."""
        return self._config.get('TELEGRAM_BOT_TOKEN') or os.environ.get('TELEGRAM_BOT_TOKEN', '')
    
    @property
    def TRADINGVIEW_USERNAME(self) -> str:
        """Get the TradingView username."""
        return self._config.get('TRADINGVIEW_USERNAME') or os.environ.get('TRADINGVIEW_USERNAME', '')
    
    @property
    def TRADINGVIEW_PASSWORD(self) -> str:
        """Get the TradingView password."""
        return self._config.get('TRADINGVIEW_PASSWORD') or os.environ.get('TRADINGVIEW_PASSWORD', '')
    
    @property
    def SUPPORTED_INSTRUMENTS(self) -> List[str]:
        """Get the list of supported instruments."""
        default = ['eurusd', 'gbpusd', 'usdjpy', 'audusd']
        from_config = self._config.get('SUPPORTED_INSTRUMENTS', [])
        from_env = os.environ.get('SUPPORTED_INSTRUMENTS')
        
        if from_env:
            try:
                return [i.strip().lower() for i in from_env.split(',')]
            except:
                logger.error("Error parsing SUPPORTED_INSTRUMENTS from environment")
        
        return from_config or default
    
    @property
    def SUPPORTED_MARKETS(self) -> Dict[str, List[str]]:
        """Get the mapping of supported markets for each instrument."""
        default = {
            'eurusd': ['forex'],
            'gbpusd': ['forex'],
            'usdjpy': ['forex'],
            'audusd': ['forex'],
            # Add more defaults as needed
        }
        
        from_config = self._config.get('SUPPORTED_MARKETS', {})
        
        # Merge defaults with config, preferring config values
        result = default.copy()
        result.update(from_config)
        
        return result 