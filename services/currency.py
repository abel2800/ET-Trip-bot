"""Currency conversion service for USD to ETB."""

import requests
from typing import Optional
import logging
from datetime import datetime, timedelta

from config.settings import settings

logger = logging.getLogger(__name__)


class CurrencyConverter:
    """Service for converting USD to Ethiopian Birr (ETB)."""
    
    def __init__(self):
        self.api_url = settings.CURRENCY_API_URL
        self.fallback_rate = settings.USD_TO_ETB_RATE
        self._cache = {}
        self._cache_timestamp = None
        self._cache_duration = timedelta(hours=6)  # Cache for 6 hours
    
    def get_usd_to_etb_rate(self) -> float:
        """
        Get current USD to ETB exchange rate.
        
        Returns:
            Exchange rate as float
        """
        # Check cache
        if self._is_cache_valid():
            return self._cache.get('USD_ETB', self.fallback_rate)
        
        # Fetch from API
        try:
            response = requests.get(
                f"{self.api_url}/latest",
                params={'base': 'USD', 'symbols': 'ETB'},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if 'rates' in data and 'ETB' in data['rates']:
                rate = float(data['rates']['ETB'])
                
                # Update cache
                self._cache['USD_ETB'] = rate
                self._cache_timestamp = datetime.now()
                
                logger.info(f"Updated USD to ETB rate: {rate}")
                return rate
            else:
                logger.warning("Currency API response missing rate data")
                return self.fallback_rate
        
        except requests.RequestException as e:
            logger.error(f"Currency API error: {e}")
            return self.fallback_rate
    
    def convert_usd_to_etb(self, usd_amount: float) -> float:
        """
        Convert USD amount to ETB.
        
        Args:
            usd_amount: Amount in USD
        
        Returns:
            Amount in ETB
        """
        rate = self.get_usd_to_etb_rate()
        etb_amount = usd_amount * rate
        return round(etb_amount, 2)
    
    def convert_etb_to_usd(self, etb_amount: float) -> float:
        """
        Convert ETB amount to USD.
        
        Args:
            etb_amount: Amount in ETB
        
        Returns:
            Amount in USD
        """
        rate = self.get_usd_to_etb_rate()
        usd_amount = etb_amount / rate
        return round(usd_amount, 2)
    
    def _is_cache_valid(self) -> bool:
        """
        Check if cached rate is still valid.
        
        Returns:
            True if cache is valid, False otherwise
        """
        if self._cache_timestamp is None:
            return False
        
        age = datetime.now() - self._cache_timestamp
        return age < self._cache_duration
    
    def format_price(self, amount: float, currency: str = "ETB") -> str:
        """
        Format price with currency symbol.
        
        Args:
            amount: Price amount
            currency: Currency code
        
        Returns:
            Formatted price string
        """
        if currency == "ETB":
            return f"{amount:,.2f} Birr"
        elif currency == "USD":
            return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"


