import logging
from config import settings
from http_client import CMCHTTPClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def init_cmc_client():
    try:
        client = await CMCHTTPClient(
            base_url="https://pro-api.coinmarketcap.com",
            api_key=settings.CMC_API_KEY,
            service="CMC_PRO"
        ).__aenter__()
        logger.info("CMC client initialized successfully")
        return client
    except Exception as e:
        logger.exception(f"Failed to initialize CMC client: {e}")
        return None

async def close_cmc_client(client):
    if client:
        try:
            await client.__aexit__(None, None, None)
            logger.info("CMC client closed successfully")
        except Exception as e:
            logger.exception(f"Failed to close CMC client: {e}")