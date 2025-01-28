from abc import ABC, abstractmethod
from typing import List, Dict, Any
import aiohttp
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from ..config import settings
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseScraper(ABC):
    def __init__(self):
        self.user_agent = UserAgent()
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_page(self, url: str, params: Dict[str, Any] = None) -> str:
        session = await self.get_session()
        headers = {"User-Agent": self.user_agent.random}
        
        async with session.get(
            url,
            params=params,
            headers=headers,
            timeout=settings.REQUEST_TIMEOUT
        ) as response:
            if response.status == 200:
                return await response.text()
            raise Exception(f"Failed to fetch {url}: {response.status}")
    
    @abstractmethod
    async def search_flights(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def search_accommodations(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None