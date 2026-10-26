import requests
import pandas as pd
import string
import time
import random
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from urllib.parse import quote_plus
import logging
from datetime import datetime
from typing import List, Dict, Optional, Set
import concurrent.futures
from tqdm import tqdm
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class SEOKeywordMiner:
    """
    SEO Keyword Mining Tool
    
    This class automatically collects search keywords related to a topic
    using several Google data sources.
    
    Data sources used:
    - Google Autocomplete suggestions
    - Google People Also Ask questions
    - Google Trends interest data
    - Related searches (bottom of Google SERP)
    """
    
    def __init__(self, delay: float = 0.5, max_workers: int = 5):
        """
        Initialize the SEO Keyword Miner.
        
        Args:
            delay: Delay between requests to avoid rate limiting
            max_workers: Maximum number of concurrent threads for trend fetching
        """
        self.delay = delay
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        })
        
    def google_autocomplete(self, query: str) -> List[str]:
        """
        Query Google Autocomplete and return suggested searches.
        
        Args:
            query: Search phrase used as input
            
        Returns:
            List of autocomplete keyword suggestions
        """
        try:
            url = "https://suggestqueries.google.com/complete/search"
            params = {
                "client": "firefox",
                "q": query,
                "hl": "es"  # Spanish language suggestions
            }
            
            r = self.session.get(url, params=params, timeout=5)
            
            if r.status_code == 200:
                return r.json()[1]
            else:
                logger.warning(f"Autocomplete returned status {r.status_code} for query: {query}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in autocomplete for '{query}': {str(e)}")
            return []
    
    def expand_keywords(self, seed: str) -> Set[str]:
        """
        Expand a seed keyword by querying Google Autocomplete
        with letters a–z and common prepositions.
        
        Args:
            seed: Base keyword
            
        Returns:
            Set of unique expanded keyword suggestions
        """
        keywords = set()
        expansions = []
        
        # Add letters a-z
        expansions.extend([f"{seed} {letter}" for letter in string.ascii_lowercase])
        
        # Add common question words and prepositions (Spanish-focused)
        expansions.extend([
            f"{seed} como", f"{seed} cuanto", f"{seed} donde", 
            f"{seed} cuando", f"{seed} porque", f"{seed} para",
            f"{seed} requisitos", f"{seed} beneficios", f"{seed} precio",
            f"{seed} costo", f"{seed} vs", f"{seed} o"
        ])
        
        # Add number variations
        expansions.extend([f"{seed} 2024", f"{seed} 2025"])
        
        logger.info(f"Expanding '{seed}' with {len(expansions)} variations")
        
        for i, query in enumerate(expansions):
            try:
                results = self.google_autocomplete(query)
                keywords.update(results)
                
                # Adaptive delay
                time.sleep(self.delay + random.uniform(0, 0.3))
                
                # Progress indicator every 10 queries
                if (i + 1) % 10 == 0:
                    logger.debug(f"Processed {i + 1}/{len(expansions)} expansions for '{seed}'")
                    
            except Exception as e:
                logger.error(f"Error expanding '{query}': {str(e)}")
                continue
        
        logger.info(f"Found {len(keywords)} unique keywords for '{seed}'")
        return keywords
    
    def people_also_ask(self, query: str) -> List[str]:
        """
        Extract questions from Google's 'People Also Ask' section.
        
        Args:
            query: Search query used to retrieve a Google results page
            
        Returns:
            List of related questions shown by Google
        """
        questions = set()
        
        try:
            url = f"https://www.google.com/search?q={quote_plus(query)}&hl=es"
            r = self.session.get(url, timeout=10)
            
            if r.status_code != 200:
                logger.warning(f"People Also Ask returned status {r.status_code} for '{query}'")
                return []
            
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Multiple selectors for PAA questions (Google changes these)
            selectors = [
                "div[jsname='Cpkphb']",
                "div.related-question-pair",
                "div[data-hveid] div[role='heading']",
                "div.wQiwMc",  # Another common PAA class
            ]
            
            for selector in selectors:
                for element in soup.select(selector):
                    text = element.get_text().strip()
                    if text and len(text) > 10 and "?" in text:
                        questions.add(text)
            
            # Also try to find questions in the page
            for element in soup.find_all(['h3', 'div'], class_=re.compile(r'question|heading', re.I)):
                text = element.get_text().strip()
                if text and len(text) > 15 and "?" in text:
                    questions.add(text)
            
            logger.debug(f"Found {len(questions)} PAA questions for '{query}'")
            
        except Exception as e:
            logger.error(f"Error extracting PAA for '{query}': {str(e)}")
        
        return list(questions)
    
    def related_searches(self, query: str) -> List[str]:
        """
        Extract related searches from the bottom of Google SERP.
        
        Args:
            query: Search query
            
        Returns:
            List of related search terms
        """
        related = set()
        
        try:
            url = f"https://www.google.com/search?q={quote_plus(query)}&hl=es"
            r = self.session.get(url, timeout=10)
            
            if r.status_code != 200:
                return []
            
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Related searches selectors
            selectors = [
                "div.s75CSd a",
                "div[data-attrid='related searches'] a",
                "div.brs_col p a",
            ]
            
            for selector in selectors:
                for element in soup.select(selector):
                    text = element.get_text().strip()
                    if text and len(text) > 5:
                        related.add(text)
            
            logger.debug(f"Found {len(related)} related searches for '{query}'")
            
        except Exception as e:
            logger.error(f"Error extracting related searches for '{query}': {str(e)}")
        
        return list(related)
    
    @staticmethod
    def classify_intent(keyword: str) -> str:
        """
        Classify the search intent of a keyword.
        
        Categories:
        - Informacional: user is looking for information
        - Comercial: user is evaluating services/products
        - Transaccional: user is likely ready to purchase/act
        - Navegacional: user is looking for a specific website
        
        Args:
            keyword: The keyword to classify
            
        Returns:
            Intent category
        """
        k = keyword.lower()
        
        # Transaccional
        transactional_indicators = [
            "precio", "cost", "costo", "price", "tarifa", "comprar", 
            "buy", "order", "contratar", "pagar", "payment", "fee",
            "cuanto cuesta", "presupuesto", "quote", "costo"
        ]
        if any(x in k for x in transactional_indicators):
            return "Transaccional"
        
        # Comercial
        commercial_indicators = [
            "servicio", "lawyer", "abogado", "consultor", "consultoría",
            "asesor", "mejor", "best", "top", "review", "reseña",
            "opiniones", "reviews", "vs", "versus", "comparar"
        ]
        if any(x in k for x in commercial_indicators):
            return "Comercial"
        
        # Navegacional
        navigational_indicators = [
            ".com", ".py", ".gov", ".org", "sitio", "web", "website",
            "oficial", "official", "pagina", "home", "inicio"
        ]
        if any(x in k for x in navigational_indicators):
            return "Navegacional"
        
        # Default to Informacional
        return "Informacional"
    
    def get_trend_score(self, keyword: str, retries: int = 2) -> Optional[int]:
        """
        Retrieve an average interest score for a keyword using Google Trends.
        
        Args:
            keyword: The keyword to check
            retries: Number of retry attempts
            
        Returns:
            Average trend score (0-100) or None if unavailable
        """
        for attempt in range(retries):
            try:
                pytrends = TrendReq(hl='es-ES', tz=360)
                pytrends.build_payload([keyword], timeframe='today 12-m')
                data = pytrends.interest_over_time()
                
                if not data.empty:
                    score = int(data[keyword].mean())
                    logger.debug(f"Trend score for '{keyword}': {score}")
                    return score
                
                return None
                
            except ResponseError as e:
                logger.warning(f"Trends response error for '{keyword}' (attempt {attempt + 1}): {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
                
            except Exception as e:
                logger.error(f"Error getting trend score for '{keyword}': {str(e)}")
                return None
        
        return None
    
    def batch_get_trend_scores(self, keywords: List[str]) -> Dict[str, Optional[int]]:
        """
        Get trend scores for multiple keywords concurrently.
        
        Args:
            keywords: List of keywords to check
            
        Returns:
            Dictionary mapping keywords to trend scores
        """
        scores = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_keyword = {
                executor.submit(self.get_trend_score, keyword): keyword 
                for keyword in keywords
            }
            
            for future in tqdm(concurrent.futures.as_completed(future_to_keyword), 
                             total=len(keywords), 
                             desc="Fetching trend scores"):
                keyword = future_to_keyword[future]
                try:
                    scores[keyword] = future.result()
                except Exception as e:
                    logger.error(f"Error processing '{keyword}': {str(e)}")
                    scores[keyword] = None
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
        
        return scores
    
    def mine_keywords(self, seeds: List[str], include_related: bool = True) -> pd.DataFrame:
        """
        Main mining pipeline.
        
        Args:
            seeds: List of seed keywords to expand
            include_related: Whether to include related searches
            
        Returns:
            DataFrame with mined keywords and metrics
        """
        all_keywords = set()
        
        # Phase 1: Expand seeds with autocomplete
        logger.info(f"Phase 1: Expanding {len(seeds)} seed keywords")
        for seed in seeds:
            expanded = self.expand_keywords(seed)
            all_keywords.update(expanded)
            
            # Add PAA questions
            paa = self.people_also_ask(seed)
            all_keywords.update(paa)
            
            # Add related searches
            if include_related:
                related = self.related_searches(seed)
                all_keywords.update(related)
        
        logger.info(f"Total unique keywords collected: {len(all_keywords)}")
        
        # Phase 2: Filter and clean keywords
        cleaned_keywords = self.clean_keywords(list(all_keywords))
        logger.info(f"After cleaning: {len(cleaned_keywords)} keywords")
        
        # Phase 3: Get trend scores (batch)
        logger.info("Phase 3: Fetching trend scores")
        trend_scores = self.batch_get_trend_scores(cleaned_keywords)
        
        # Phase 4: Build DataFrame
        rows = []
        for keyword in cleaned_keywords:
            rows.append({
                "keyword": keyword,
                "intent": self.classify_intent(keyword),
                "trend_score": trend_scores.get(keyword),
                "length": len(keyword),
                "word_count": len(keyword.split()),
                "has_question": 1 if "?" in keyword else 0
            })
        
        df = pd.DataFrame(rows)
        
        # Sort by trend score (highest first)
        df = df.sort_values("trend_score", ascending=False, na_position="last")
        
        return df
    
    @staticmethod
    def clean_keywords(keywords: List[str]) -> List[str]:
        """
        Clean and filter keywords.
        
        Args:
            keywords: List of raw keywords
            
        Returns:
            Cleaned and filtered keywords
        """
        cleaned = set()
        
        for k in keywords:
            # Remove empty or very short keywords
            if not k or len(k) < 4:
                continue
            
            # Remove duplicates (case insensitive)
            k_lower = k.lower().strip()
            
            # Remove URLs and email addresses
            if 'http' in k_lower or '@' in k_lower:
                continue
            
            # Remove excessive punctuation
            k_clean = re.sub(r'[^\w\s¿?¡!]', ' ', k)
            k_clean = re.sub(r'\s+', ' ', k_clean).strip()
            
            if k_clean and len(k_clean) >= 4:
                cleaned.add(k_clean)
        
        return list(cleaned)
    
    def export_report(self, df: pd.DataFrame, filename: str = None):
        """
        Export the keyword dataset with summary statistics.
        
        Args:
            df: DataFrame with keywords
            filename: Output filename (optional)
        """
        if filename is None:
            filename = f"seo_keywords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Create a summary sheet
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main keywords sheet
            df.to_excel(writer, sheet_name='Keywords', index=False)
            
            # Summary statistics sheet
            summary = pd.DataFrame({
                'Metric': [
                    'Total Keywords',
                    'Informational',
                    'Commercial',
                    'Transactional',
                    'Navigational',
                    'With Trend Score',
                    'Avg Trend Score',
                    'Questions'
                ],
                'Value': [
                    len(df),
                    len(df[df['intent'] == 'Informacional']),
                    len(df[df['intent'] == 'Comercial']),
                    len(df[df['intent'] == 'Transaccional']),
                    len(df[df['intent'] == 'Navegacional']),
                    len(df[df['trend_score'].notna()]),
                    int(df['trend_score'].mean()) if df['trend_score'].notna().any() else 0,
                    df['has_question'].sum()
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Intent distribution sheet
            intent_dist = df['intent'].value_counts().reset_index()
            intent_dist.columns = ['Intent', 'Count']
            intent_dist.to_excel(writer, sheet_name='Intent Distribution', index=False)
        
        logger.info(f"Report exported to: {filename}")
        return filename


def main():
    """
    Main execution function.
    """
    import re  # Import here for the clean_keywords method
    
    # Configuration
    seeds = [
        "residencia fiscal paraguay",
        "paraguay tax residency",
        "mudarse a paraguay",
        "vivir en paraguay",
        "impuestos paraguay",
        "requisitos residencia paraguay"
    ]
    
    # Initialize miner
    miner = SEOKeywordMiner(delay=0.5, max_workers=3)
    
    logger.info("=" * 60)
    logger.info("SEO KEYWORD MINING TOOL")
    logger.info("=" * 60)
    
    try:
        # Mine keywords
        logger.info(f"Starting keyword mining with {len(seeds)} seed keywords")
        df = miner.mine_keywords(seeds, include_related=True)
        
        # Display results
        logger.info("\n" + "=" * 60)
        logger.info("MINING RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total keywords found: {len(df)}")
        logger.info("\nIntent distribution:")
        print(df['intent'].value_counts())
        logger.info(f"\nKeywords with trend scores: {df['trend_score'].notna().sum()}")
        
        # Export
        filename = miner.export_report(df)
        
        # Show top keywords by trend score
        logger.info("\nTop 10 keywords by trend score:")
        top_keywords = df[df['trend_score'].notna()].head(10)
        for idx, row in top_keywords.iterrows():
            print(f"  {row['keyword']} (Score: {row['trend_score']}, Intent: {row['intent']})")
        
        logger.info(f"\n Process completed successfully!")
        logger.info(f" Report saved to: {filename}")
        
    except Exception as e:
        logger.error(f" Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()