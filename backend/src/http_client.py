from aiohttp import ClientSession
from async_lru import alru_cache
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self, base_url: str, api_key: str, service: str):
        self._base_url = base_url
        self._api_key = api_key
        self._service = service
        self._session = None

    async def __aenter__(self):
        self._session = ClientSession(
            base_url=self._base_url,
            headers={
                f'X-{self._service.upper()}_API_KEY': self._api_key,
            }
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()

    @property
    def session(self):
        if not self._session:
            raise RuntimeError("Session is not initialized, use 'async with HTTPClient()' context manager")
        return self._session

class CMCHTTPClient(HTTPClient):
    @alru_cache
    async def get_listings(self):
        logger.debug("Fetching listings...")
        try:
            async with self.session.get("/v1/cryptocurrency/listings/latest") as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    logger.error(f"Error response from CMC API: {error_text}")
                    raise Exception(f"CMC API returned status {resp.status}: {error_text}")
                result = await resp.json()
                logger.debug(f"Listings fetched: {result}")
                return result["data"]
        except Exception as e:
            logger.exception(f"Exception in get_listings: {str(e)}")
            raise

    @alru_cache
    async def get_currency(self, currency_id: int):
        logger.debug(f"Fetching currency with ID: {currency_id}")
        try:
            async with self.session.get(
                "/v2/cryptocurrency/quotes/latest",
                params={"id": currency_id}
            ) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    logger.error(f"Error response from CMC API: {error_text}")
                    raise Exception(f"CMC API returned status {resp.status}: {error_text}")
                result = await resp.json()
                logger.debug(f"Currency fetched: {result}")
                return result["data"][str(currency_id)]
        except Exception as e:
            logger.exception(f"Exception in get_currency: {str(e)}")
            raise