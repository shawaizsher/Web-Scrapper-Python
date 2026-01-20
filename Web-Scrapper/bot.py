import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
from textblob import TextBlob
from bs4 import BeautifulSoup
import re


class WebScraperBot:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def navigate_to(self, url):
        self.driver.get(url)

    def get_element_text(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element.text
        except NoSuchElementException:
            return None

    def click_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            element.click()
        except NoSuchElementException:
            pass

    def get_page_text(self):
        """Get all text content from the current page"""
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=' ', strip=True)
            return text
        except Exception as e:
            print(f"Error extracting page text: {e}")
            return None

    def extract_relevant_text(self, text, prompt, max_snippets=5):
        """Extract sentences from text that match the prompt keywords
        Returns: string with top matching sentences"""
        if not text or not prompt:
            return None
        prompt_terms = [w.lower() for w in re.findall(r"\w+", prompt) if len(w) > 2]
        if not prompt_terms:
            return None
        sentences = re.split(r'(?<=[.!?])\s+', text)
        scored = []
        for sentence in sentences:
            lowered = sentence.lower()
            score = sum(lowered.count(term) for term in prompt_terms)
            if score > 0:
                scored.append((score, sentence.strip()))
        scored.sort(key=lambda x: x[0], reverse=True)
        snippets = [s for _, s in scored[:max_snippets]]
        return " ".join(snippets) if snippets else None

    def analyze_sentiment(self, text):
        """Analyze sentiment of given text
        Returns: dict with polarity, subjectivity, and sentiment classification"""
        if not text:
            return None
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment based on polarity with better thresholds
        if polarity > 0.15:
            sentiment_class = "Positive"
        elif polarity < -0.15:
            sentiment_class = "Negative"
        else:
            sentiment_class = "Neutral"
        
        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "sentiment": sentiment_class,
            "text_preview": text[:200] + "..." if len(text) > 200 else text
        }

    def scrape_and_analyze(self, url, element_selector=None, by=By.TAG_NAME, prompt=None):
        """Scrape specific element(s) and analyze sentiment
        Returns: dict with scraped content and sentiment analysis"""
        try:
            self.navigate_to(url)
            time.sleep(2)  # Wait for page to load
            
            if element_selector:
                elements = self.driver.find_elements(by, element_selector)
                content = " ".join([elem.text for elem in elements if elem.text])
            else:
                content = self.get_page_text() or ""
            
            sentiment = self.analyze_sentiment(content)
            prompt_matches = self.extract_relevant_text(content, prompt) if prompt else None
            
            return {
                "url": url,
                "content_length": len(content),
                "content_preview": content[:300] + "..." if len(content) > 300 else content,
                "sentiment": sentiment,
                "prompt_matches": prompt_matches
            }
        except Exception as e:
            print(f"Error during scraping and analysis: {e}")
            return None

    def close(self):
        self.driver.quit()
