import logging
from fastapi import APIRouter, HTTPException, Request

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cryptocurrencies")

@router.get("")
async def get_cryptocurrencies(request: Request):
    cmc_client = request.app.state.cmc_client
    if cmc_client is None:
        logger.error("CMC client is not initialized")
        raise HTTPException(status_code=500, detail="CMC client is not initialized")
    try:
        listings = await cmc_client.get_listings()
        logger.info(f"Listings response in route: {listings}")
        return listings
    except Exception as e:
        logger.exception(f"Failed to fetch listings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch listings: {str(e)}")

@router.get("/{currency_id}")
async def get_cryptocurrency(currency_id: int, request: Request):
    cmc_client = request.app.state.cmc_client
    if cmc_client is None:
        logger.error("CMC client is not initialized")
        raise HTTPException(status_code=500, detail="CMC client is not initialized")
    try:
        currency = await cmc_client.get_currency(currency_id)
        logger.info(f"Currency response in route: {currency}")
        return currency
    except Exception as e:
        logger.exception(f"Failed to fetch currency: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch currency: {str(e)}")