import sys
import os

try:
    import aiohttp
    print(f"Successfully imported aiohttp version: {aiohttp.__version__}")
except Exception as e:
    print(f"Error importing aiohttp: {e}")
    import traceback
    traceback.print_exc() 