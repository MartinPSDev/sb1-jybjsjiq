from .base import BaseScraper
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class KayakScraper(BaseScraper):
    BASE_URL = "https://www.kayak.com.ar"
    
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        search_params = {
            "q": params["destination"],
            "checkin": params["start_date"].strftime("%Y-%m-%d"),
            "checkout": params["end_date"].strftime("%Y-%m-%d"),
            "adults": str(params["guests"]),
            "price": f"0-{params['budget']}"
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/hotels/{params['destination']}",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for hotel in soup.select('[class*="HotelResultCard"]'):
            try:
                title = hotel.select_one('[class*="HotelName"]').text.strip()
                price_element = hotel.select_one('[class*="PropertyCardPrice"]')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                image = hotel.select_one('img')
                image_url = image['src'] if image else None
                
                rating = hotel.select_one('[class*="ReviewScore"]')
                rating = float(rating.text.strip().split('/')[0]) if rating else None
                
                link = hotel.select_one('a')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Kayak",
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
                print(f"Error parsing Kayak hotel: {e}")
                continue
        
        return results
    
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not params.get("origin"):
            return []
            
        search_params = {
            "origin": params["origin"],
            "destination": params["destination"],
            "depart": params["start_date"].strftime("%Y-%m-%d"),
            "return": params["end_date"].strftime("%Y-%m-%d"),
            "travelers": str(params["guests"])
        }
        
        html = await self.fetch_page(
            f"{self.BASE_URL}/flights",
            params=search_params
        )
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for flight in soup.select('[class*="FlightResultCard"]'):
            try:
                airline = flight.select_one('[class*="AirlineName"]').text.strip()
                price_element = flight.select_one('[class*="Price"]')
                price = float(price_element.text.strip().replace('$', '').replace('.', '').replace(',', '.'))
                
                duration = flight.select_one('[class*="Duration"]').text.strip()
                stops = flight.select_one('[class*="Stops"]').text.strip()
                
                link = flight.select_one('a')
                full_link = urljoin(self.BASE_URL, link['href']) if link else None
                
                results.append({
                    "site": "Kayak",
                    "type": "flight",
                    "title": f"{airline} - {stops}",
                    "price": price,
                    "currency": "USD",
                    "link": full_link,
                    "description": f"Duration: {duration}, Stops: {stops}"
                })
            except Exception as e:
                print(f"Error parsing Kayak flight: {e}")
                continue
        
        return results