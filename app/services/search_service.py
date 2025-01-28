from typing import List, Dict, Any
from ..scrapers.booking import BookingScraper
from ..scrapers.airbnb import AirbnbScraper
from ..scrapers.despegar import DespegarScraper
from ..scrapers.kayak import KayakScraper
from ..scrapers.expedia import ExpediaScraper
from ..models import Search, SearchResult
from sqlalchemy.orm import Session
import asyncio
from datetime import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class SearchService:
    def __init__(self):
        self.scrapers = [
            BookingScraper(),
            AirbnbScraper(),
            DespegarScraper(),
            KayakScraper(),
            ExpediaScraper()
        ]
    
    async def search_all(self, db: Session, search_params: Dict[str, Any]) -> Dict[str, Any]:
        # Create search record
        search = Search(
            user_id=search_params.get("user_id"),
            destination=search_params["destination"],
            start_date=search_params["start_date"],
            end_date=search_params["end_date"],
            guests=search_params["guests"],
            budget=search_params["budget"],
            origin=search_params.get("origin")
        )
        db.add(search)
        db.commit()
        
        # Gather results from all scrapers concurrently
        tasks = []
        for scraper in self.scrapers:
            tasks.extend([
                asyncio.create_task(scraper.search_accommodations(search_params)),
                asyncio.create_task(scraper.search_flights(search_params))
            ])
        
        # Wait for all scraping tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results, filtering out exceptions
        all_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error during scraping: {result}")
                continue
            if isinstance(result, list):
                all_results.extend(result)
        
        # Close all scraper sessions
        for scraper in self.scrapers:
            await scraper.close()
        
        # Process and store results
        processed_results = self._process_results(db, search.id, all_results)
        
        return {
            "id": search.id,
            "best_flight": processed_results["best_flight"],
            "best_accommodation": processed_results["best_accommodation"],
            "all_flights": processed_results["flights"],
            "all_accommodations": processed_results["accommodations"],
            "total_found": len(all_results),
            "created_at": datetime.utcnow()
        }
    
    def _process_results(self, db: Session, search_id: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        flights = [r for r in results if r["type"] == "flight"]
        accommodations = [r for r in results if r["type"] == "accommodation"]
        
        # Store results in database
        for result in results:
            db_result = SearchResult(
                search_id=search_id,
                **result
            )
            db.add(db_result)
        db.commit()
        
        # Find best options using a scoring system
        best_flight = self._find_best_option(flights) if flights else None
        best_accommodation = self._find_best_option(accommodations) if accommodations else None
        
        return {
            "flights": flights,
            "accommodations": accommodations,
            "best_flight": best_flight,
            "best_accommodation": best_accommodation
        }
    
    def _find_best_option(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not options:
            return None
        
        # Create features matrix
        features = []
        for option in options:
            price = option["price"]
            rating = option.get("rating", 0)
            reviews = option.get("reviews_count", 0)
            features.append([price, rating, reviews])
        
        # Normalize features
        scaler = MinMaxScaler()
        normalized_features = scaler.fit_transform(features)
        
        # Calculate scores (lower price is better, higher rating and reviews are better)
        scores = normalized_features[:, 0] * -0.5 + normalized_features[:, 1] * 0.3 + normalized_features[:, 2] * 0.2
        
        # Return option with best score
        best_index = np.argmax(scores)
        return options[best_index]