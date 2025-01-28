from .base import BaseScraper
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class BookingScraper(BaseScraper):
    BASE_URL = "https://www.booking.com"
    
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_params = {
            "ss": params["destination"],
            "checkin": params["start_date"].strftime("%Y-%m-%d"),
            "checkout": params["end_date"].strftime("%Y-%m-%d"),
            "group_adults": str(params["guests"]),
            "no_rooms": "1",
            "nflt": f"price=0-{params['budget']}"
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/searchresults.html",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for property_card in soup.select('[data-testid="property-card"]'):
            try:
                title = property_card.select_one('[data-testid="title"]').text.strip()
                price_element = property_card.select_one('[data-testid="price-and-discounted-price"]')
                price = float(price_element.text.strip().replace('$', '').replace(',', ''))
                
                image = property_card.select_one('img')
                image_url = image['src'] if image else None
                
                rating = property_card.select_one('[data-testid="rating-score"]')
                rating = float(rating.text.strip()) if rating else None
                
                link = property_card.select_one('a[href*="hotel"]')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Booking.com",
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
                print(f"Error parsing property card: {e}")
                continue
        
        return results
    
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Booking.com doesn't offer flights directly
        return []