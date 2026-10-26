import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urlparse
import re
from datetime import datetime

class CompetitorAnalyzer:
    def __init__(self, delay=2):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_word_count(self, soup):
        """Get word count from soup object"""
        if not soup:
            return None
        text = soup.get_text().split()
        return len(text)
    
    def classify_content_type(self, soup, html):
        """Classify the type of content"""
        h = html.lower()
        
        if soup.find('article') or "<article" in h:
            return "article"
        if soup.find_all(['ol', 'ul']) and len(soup.find_all(['ol', 'ul'])) > 2:
            return "list"
        if "faq" in h or soup.find(class_=re.compile(r'faq', re.I)):
            return "faq"
        if soup.find('form') or soup.find('input'):
            return "interactive/tool"
        if len(soup.find_all(['h1', 'h2', 'h3'])) > 5:
            return "structured_guide"
        if soup.find('table'):
            return "comparison_table"
        if len(soup.get_text()) < 500:
            return "brief_overview"
        
        return "general_article"
    
    def analyze_strengths(self, title, word_count, content_type, domain):
        """Identify potential strengths of the content"""
        strengths = []
        
        if word_count and word_count > 1500:
            strengths.append("Comprehensive content (>1500 words)")
        elif word_count and word_count > 800:
            strengths.append("Good content depth")
        
        if content_type in ["structured_guide", "comparison_table"]:
            strengths.append("Well-structured information")
        
        if "blog" in domain:
            strengths.append("Blog format (regular updates likely)")
        elif ".gov" in domain or ".edu" in domain:
            strengths.append("High authority domain")
        
        if "residencia" in title.lower() or "tax" in title.lower():
            strengths.append("Highly relevant title")
            
        return strengths if strengths else ["Basic content structure"]
    
    def analyze_page(self, url):
        """Comprehensive page analysis"""
        try:
            time.sleep(self.delay + random.uniform(0, 1))
            
            r = self.session.get(url, timeout=10)
            html = r.text
            soup = BeautifulSoup(html, "html.parser")
            
            title = soup.title.string.strip() if soup.title else ""
            domain = urlparse(url).netloc
            word_count = self.get_word_count(soup)
            content_type = self.classify_content_type(soup, html)
            
            # Heading structure
            h1_count = len(soup.find_all('h1'))
            h2_count = len(soup.find_all('h2'))
            
            # Strengths analysis
            strengths = self.analyze_strengths(title, word_count, content_type, domain)
            
            return {
                'url': url,
                'domain': domain,
                'title': title,
                'word_count': word_count,
                'content_type': content_type,
                'h1_count': h1_count,
                'h2_count': h2_count,
                'strengths': ', '.join(strengths),
                'backlinks': "N/A (Use Ahrefs/Moz for accurate data)",
                'status': 'Success'
            }
            
        except Exception as e:
            return {
                'url': url, 
                'status': f'Error: {str(e)[:50]}', 
                'word_count': None, 
                'domain': urlparse(url).netloc
            }
    
    def analyze_competitors(self, urls):
        """Analyze a list of URLs"""
        print(f"Analyzing {len(urls)} URLs...")
        print("-" * 50)
        
        rows = []
        for i, url in enumerate(urls, 1):
            print(f"  Analyzing {i}/{len(urls)}: {url[:60]}...")
            data = self.analyze_page(url)
            if data:
                rows.append(data)
        
        return rows
    
    def generate_report(self, rows):
        """Generate a comprehensive report"""
        if not rows:
            print("\nNo data to analyze.")
            return None
        
        df = pd.DataFrame(rows)
        
        # Filter successful analyses
        df_success = df[df['status'] == 'Success'].copy() if 'status' in df.columns else df.copy()
        df_failed = df[df['status'] != 'Success'] if 'status' in df.columns and len(df[df['status'] != 'Success']) > 0 else pd.DataFrame()
        
        print("\n" + "="*80)
        print("COMPETITIVE ANALYSIS REPORT")
        print("="*80)
        
        # 1. Which websites are ranking?
        print("\n1. TOP RANKING WEBSITES ANALYZED:")
        print("-" * 50)
        if len(df_success) > 0:
            for idx, row in df_success.iterrows():
                print(f"{idx+1}. {row.get('domain', 'Unknown')}")
                print(f"   URL: {row.get('url', 'N/A')[:80]}")
                print(f"   Title: {row.get('title', 'N/A')[:80]}")
                print()
        else:
            print("  No successful page analyses")
        
        # 2. What type of content do they have?
        print("\n2. CONTENT TYPE DISTRIBUTION:")
        print("-" * 50)
        if 'content_type' in df_success.columns and len(df_success) > 0:
            content_types = df_success['content_type'].value_counts()
            for ctype, count in content_types.items():
                print(f"  - {ctype}: {count} sites")
        else:
            print("  No content type data available")
        
        # 3. How many words do they have?
        print("\n3. WORD COUNT ANALYSIS:")
        print("-" * 50)
        if 'word_count' in df_success.columns and len(df_success['word_count'].dropna()) > 0:
            print(f"  Average: {df_success['word_count'].mean():.0f} words")
            print(f"  Median: {df_success['word_count'].median():.0f} words")
            print(f"  Min: {df_success['word_count'].min():.0f} words")
            print(f"  Max: {df_success['word_count'].max():.0f} words")
        else:
            print("  No word count data available")
        
        # 4. Backlinks note
        print("\n4. BACKLINKS:")
        print("-" * 50)
        print("  For accurate backlink data, use professional tools like:")
        print("  - Ahrefs (ahrefs.com)")
        print("  - Moz (moz.com)")
        print("  - SEMrush (semrush.com)")
        
        # 5. What do they do well?
        print("\n5. STRENGTHS ANALYSIS:")
        print("-" * 50)
        if 'strengths' in df_success.columns and len(df_success) > 0:
            all_strengths = []
            for strengths in df_success['strengths'].dropna():
                all_strengths.extend([s.strip() for s in strengths.split(',')])
            
            if all_strengths:
                strength_counts = pd.Series(all_strengths).value_counts()
                for strength, count in strength_counts.head(5).items():
                    print(f"  - {strength}: {count} sites")
            else:
                print("  No strength data available")
        else:
            print("  No strength data available")
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"competitor_analysis_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        print(f"\nFull data saved to: {filename}")
        
        return df

def main():
    print("Competitor Analysis Tool")
    print("=" * 60)
    
    # MANUALLY ADD THE URLs YOU WANT TO ANALYZE
    # Since Google search is blocked, you need to provide URLs yourself
    # Go to Google, search for "residencia fiscal Paraguay", and copy the top 10 URLs here
    
    urls_to_analyze = [
        "https://paraguaypathways.com/es/como-obtener-la-residencia-fiscal-en-paraguay-y-evitar-perderla/",
        "https://www.dnit.gov.py/web/portal-institucional/certificado-de-residencia-fiscal-para-fines-tributarios",
        "https://impuestospy.com/residencia-en-paraguay/",
        "https://www.vivirparaguay.com/residencia-fiscal-en-paraguay/",
        "https://www.mersanlaw.com/blog/residencia-fiscal-en-paraguay-requisitos-legales-y-errores-frecuentes/",
        "https://thenomadtax.com/2025/02/paraguay-0-impuestos-residencia-fiscal/",
        "https://soynomadafiscal.com/residencia-fiscal-paraguay/",
        "https://melvato.com/residencia-fiscal-en-paraguay/",
    ]
    
    # If you don't have URLs yet, you can start with a few known sites:
    if len(urls_to_analyze) == 1 and "example" in urls_to_analyze[0]:
        print("\nPlease add real URLs to analyze.")
        print("\nCommon websites for tax residency in Paraguay:")
        print("- https://www.grantthornton.com.py/")
        print("- https://www.pwc.com.py/")
        print("- https://www.deloitte.com/py/")
        print("- https://www.ey.com/es_py/")
        print("- https://www.bcp.gov.py/")
        print("- https://www.set.gov.py/")
        print("- https://www.larazon.com.py/")
        print("- https://www.abc.com.py/")
        print("\nAdd these URLs to the 'urls_to_analyze' list in the script.")
        return
    
    # Initialize analyzer
    analyzer = CompetitorAnalyzer(delay=2)
    
    # Run analysis
    results = analyzer.analyze_competitors(urls_to_analyze)
    
    # Generate report
    df = analyzer.generate_report(results)
    
    if df is not None and len(df) > 0:
        print("\nRECOMMENDATIONS:")
        print("-" * 50)
        print("Based on the analysis, consider:")
        print("1. Create comprehensive content (>1500 words)")
        print("2. Use a clear structure with H1, H2 headings")
        print("3. Include comparison tables or structured guides")
        print("4. Ensure your title includes key terms")
        print("5. Build authority through quality backlinks")

if __name__ == "__main__":
    main()