import asyncio
import logging
import os
import sys

# --- Configuratie ---
# Voeg de project root toe aan het Python pad zodat we modules kunnen importeren
project_root = os.path.dirname(os.path.abspath(__file__))
# Als je het script ergens anders opslaat, pas dit pad aan:
# project_root = '/path/to/your/Sigmapips-V2-main-10' # Voorbeeld
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importeer de ChartService
try:
    from trading_bot.services.chart_service.chart import ChartService
except ImportError as e:
    print(f"Error importing ChartService: {e}")
    print(f"Zorg ervoor dat het script in de root van je project staat ({project_root}) of pas het pad aan.")
    sys.exit(1)

# Logging instellen
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_eurusd_technical_analysis():
    """
    Roept de ChartService direct aan om technische analyse voor EURUSD te testen.
    """
    logger.info("Initializing ChartService...")
    try:
        # Mogelijk moet je configuratie meegeven als de constructor dat vereist
        chart_service = ChartService()
        logger.info("ChartService initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize ChartService: {e}", exc_info=True)
        return

    instrument = "EURUSD"
    timeframe = "H1" # Kies een relevant timeframe

    logger.info(f"--- Testing Technical Analysis for {instrument} ({timeframe}) ---")

    # 1. Test chart generation
    try:
        logger.info(f"Requesting chart for {instrument} ({timeframe})...")
        chart_output = await chart_service.get_chart(instrument, timeframe=timeframe)
        if chart_output:
            # Output kan een path (str) of bytes zijn
            if isinstance(chart_output, str):
                logger.info(f"Chart generated successfully. Output path: {chart_output}")
                # Optioneel: check if file exists
                if os.path.exists(chart_output):
                    logger.info(f"Chart file found at: {chart_output}")
                else:
                    logger.warning(f"Chart file NOT found at expected path: {chart_output}")
            elif isinstance(chart_output, bytes):
                logger.info(f"Chart generated successfully. Output type: bytes, Length: {len(chart_output)}")
                # Optioneel: sla de bytes op om te inspecteren
                # with open(f"{instrument}_{timeframe}_test_chart.png", "wb") as f:
                #     f.write(chart_output)
                # logger.info(f"Chart saved to {instrument}_{timeframe}_test_chart.png for inspection.")
            else:
                 logger.warning(f"Chart generated but output type is unexpected: {type(chart_output)}")
        else:
            logger.error(f"Failed to generate chart for {instrument} ({timeframe}). Service returned None or empty.")

    except Exception as e:
        logger.error(f"Error during chart generation for {instrument}: {e}", exc_info=True)

    # 2. Test technical analysis text generation
    try:
        logger.info(f"Requesting technical analysis text for {instrument} ({timeframe})...")
        analysis_text = await chart_service.get_technical_analysis(instrument, timeframe=timeframe)

        if analysis_text:
            logger.info(f"Technical analysis text received:")
            # Print de output direct naar de console
            print("-" * 30)
            print(analysis_text)
            print("-" * 30)
        else:
            logger.error(f"Failed to get technical analysis text for {instrument} ({timeframe}). Service returned None or empty.")

    except Exception as e:
        logger.error(f"Error during technical analysis text generation for {instrument}: {e}", exc_info=True)

    logger.info(f"--- Test finished for {instrument} ({timeframe}) ---")

if __name__ == "__main__":
    # Zorg ervoor dat eventuele environment variables geladen zijn (indien nodig voor ChartService)
    # bijv. from dotenv import load_dotenv; load_dotenv()

    # Voer de asynchrone testfunctie uit
    try:
        asyncio.run(test_eurusd_technical_analysis())
    except KeyboardInterrupt:
        logger.info("Test interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred during the test execution: {e}", exc_info=True) 