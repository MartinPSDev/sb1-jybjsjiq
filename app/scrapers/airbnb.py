from .base import BaseScraper
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class AirbnbScraper(BaseScraper):
    BASE_URL = "https://www.airbnb.com.ar"
    
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_params = {
            "query": params["destination"],
            "checkin": params["start_date"].strftime("%Y-%m-%d"),
            "checkout": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"]),
            "price_max": str(params["budget"])
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/s/{params['destination']}/homes",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for listing in soup.select('[data-testid="card-container"]'):
            try:
                title = listing.select_one('[data-testid="listing-card-title"]').text.strip()
                price_element = listing.select_one('[data-testid="price-element"]')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                image = listing.select_one('img')
                image_url = image['src'] if image else None
                
                rating = listing.select_one('[data-testid="rating"]')
                rating = float(rating.text.strip().split()[0]) if rating else None
                
                link = listing.select_one('a')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Airbnb",
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
                print(f"Error parsing Airbnb listing: {e}")
                continue
        
        return results
    
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Airbnb doesn't offer flights
        return []