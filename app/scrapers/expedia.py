from .base import BaseScraper
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class ExpediaScraper(BaseScraper):
    BASE_URL = "https://www.expedia.com.ar"
    
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_params = {
            "destination": params["destination"],
            "startDate": params["start_date"].strftime("%Y-%m-%d"),
            "endDate": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"]),
            "maxPrice": str(params["budget"])
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/Hotel-Search",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for hotel in soup.select('[data-stid="property-listing"]'):
            try:
                title = hotel.select_one('[data-stid="property-name"]').text.strip()
                price_element = hotel.select_one('[data-stid="price-lockup"]')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                image = hotel.select_one('img')
                image_url = image['src'] if image else None
                
                rating = hotel.select_one('[data-stid="property-rating"]')
                rating = float(rating.text.strip().split('/')[0]) if rating else None
                
                link = hotel.select_one('a[data-stid="open-hotel-details"]')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Expedia",
                    "type": "accommodation",
                    "title": title,
                    "price": price,
                    "currency": "USD",
                    "link": full_link,
                    "image_url": image_url,
                    "rating": rating,
                    "description": title
                })
            except Exception as e:
                print(f"Error parsing Expedia hotel: {e}")
                continue
        
        return results
    
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not params.get("origin"):
            return []
            
        search_params = {
            "from": params["origin"],
            "to": params["destination"],
            "departing": params["start_date"].strftime("%Y-%m-%d"),
            "returning": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"])
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/Flights-Search",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for flight in soup.select('[data-test-id="flight-card"]'):
            try:
                airline = flight.select_one('[data-test-id="airline-name"]').text.strip()
                price_element = flight.select_one('[data-test-id="price-text"]')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                duration = flight.select_one('[data-test-id="duration"]').text.strip()
                stops = flight.select_one('[data-test-id="stops"]').text.strip()
                
                link = flight.select_one('a[data-test-id="select-link"]')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Expedia",
                    "type": "flight",
                    "title": f"{airline} - {stops}",
                    "price": price,
                    "currency": "USD",
                    "link": full_link,
                    "description": f"Duration: {duration}, Stops: {stops}"
                })
            except Exception as e:
                print(f"Error parsing Expedia flight: {e}")
                continue
        
        return results