from .base import BaseScraper
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class DespegarScraper(BaseScraper):
    BASE_URL = "https://www.despegar.com.ar"
    
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_params = {
            "q": params["destination"],
            "from": params["start_date"].strftime("%Y-%m-%d"),
            "to": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"]),
            "price": f"0,{params['budget']}"
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/hoteles/hl/{params['destination']}",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for hotel in soup.select('.results-cluster-container'):
            try:
                title = hotel.select_one('.accommodation-name').text.strip()
                price_element = hotel.select_one('.price-amount')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                image = hotel.select_one('.accommodation-image img')
                image_url = image['src'] if image else None
                
                rating = hotel.select_one('.rating-text')
                rating = float(rating.text.strip().split('/')[0]) if rating else None
                
                link = hotel.select_one('a.accommodation-link')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Despegar",
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
                print(f"Error parsing Despegar hotel: {e}")
                continue
        
        return results
    
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not params.get("origin"):
            return []
            
        search_params = {
            "from": params["origin"],
            "to": params["destination"],
            "departure": params["start_date"].strftime("%Y-%m-%d"),
            "return": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"])
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/vuelos",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for flight in soup.select('.cluster-container'):
            try:
                airline = flight.select_one('.airline-name').text.strip()
                price_element = flight.select_one('.price-amount')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                duration = flight.select_one('.duration').text.strip()
                stops = flight.select_one('.stops-text').text.strip()
                
                link = flight.select_one('a.flight-link')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Despegar",
                    "type": "flight",
                    "title": f"{airline} - {stops}",
                    "price": price,
                    "currency": "USD",
                    "link": full_link,
                    "description": f"Duration: {duration}, Stops: {stops}"
                })
            except Exception as e:
                print(f"Error parsing Despegar flight: {e}")
                continue
        
        return results