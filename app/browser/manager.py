import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app.core.logger import logger
from app.browser.errors import BrowserNotRunningError

BROWSER_MAX_TEXT_LENGTH = 12000
BROWSER_MAX_LINKS = 50

class BrowserManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
            cls._instance.driver = None
        return cls._instance

    def is_running(self) -> bool:
        return self.driver is not None

    def start_session(self):
        if not self.driver:
            try:
                options = Options()
                # Run headless to keep it quiet and clean for the user
                # But the prompt says "Example: JARVIS opens the page." Maybe not headless so user sees it?
                # "JARVIS opens the page" -> We will keep it non-headless for visual feedback.
                # options.add_argument("--headless")
                
                # Suppress selenium logging
                options.add_argument("--log-level=3")
                options.add_argument("--disable-notifications")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                # Set a page load timeout of 30 seconds
                self.driver.set_page_load_timeout(30)
            except Exception as e:
                logger.error(f"Failed to start Selenium session: {e}")
                raise

    def open_page(self, url: str) -> dict:
        self.start_session()
        try:
            self.driver.get(url)
            return {
                "url": self.driver.current_url,
                "title": self.driver.title
            }
        except Exception as e:
            logger.error(f"Browser navigation failed: {e}")
            raise

    def get_title(self) -> str:
        if not self.is_running():
            raise BrowserNotRunningError("No browser page is currently open.")
        return self.driver.title

    def read_page(self) -> str:
        if not self.is_running():
            raise BrowserNotRunningError("No browser page is currently open.")
            
        try:
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            # Remove scripts, styles, etc.
            for element in soup(["script", "style", "noscript", "header", "footer", "nav"]):
                element.extract()
                
            text = soup.get_text(separator=' ')
            
            # Basic cleanup: remove excessive newlines and spaces
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            if len(text) > BROWSER_MAX_TEXT_LENGTH:
                text = text[:BROWSER_MAX_TEXT_LENGTH] + "\n\n...[Content truncated due to length limits]..."
                
            return text if text else "The page appears to be blank."
        except Exception as e:
            logger.error(f"Failed to read page text: {e}")
            return "Failed to extract text from the page."

    def get_links(self) -> List[Dict[str, str]]:
        if not self.is_running():
            raise BrowserNotRunningError("No browser page is currently open.")
            
        try:
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            valid_links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text(strip=True)
                
                if text and href.lower().startswith(("http://", "https://")):
                    valid_links.append({"text": text, "url": href})
                    
                if len(valid_links) >= BROWSER_MAX_LINKS:
                    break
                    
            return valid_links
        except Exception as e:
            logger.error(f"Failed to extract links: {e}")
            return []

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None

# Global instance for JARVIS
browser_manager = BrowserManager()
