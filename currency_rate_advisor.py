import json
from typing import Dict
import urllib.request
from datetime import date

class CurrencyRateAdvisor:
    def __init__(self, openexchange_app_id: str) -> None:
        self.app_id = openexchange_app_id


    def get_currency_rates(self, base: str, target: str) -> float:
       url = self._get_openexchange_today_price_url(base, target)
       rates = self._get_rates(url)
       return rates[target]

            
    def _get_openexchange_today_price_url(self, currency_base: str, currency_target: str) -> str:
        return (
            f"https://openexchangerates.org/api/latest.json?"
            + f"app_id={self.app_id}&base={currency_base}&symbols={currency_target},)"
        )


    def _get_openexchange_historical_price_url(self, rate_date: date, currency_base: str, currency_target: str) -> str:
        return (
            f"https://openexchangerates.org/api/historical/{rate_date.strftime('%Y-%m-%d')}.json?"
            + f"app_id={self.app_id}&base={currency_base}&symbols={currency_target},)"
        )


    def _get_rates(self, url: str) -> Dict[str, float]:
        response = (urllib.request.urlopen(url).read())
        data = json.loads(response)
        return data['rates']
