"""
AgentSpace - Web Scraping & File Analysis Tools

Tools for extracting intelligence from:
1. Client websites (scraping)
2. Uploaded files (PDFs, DOCX, images)
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from pathlib import Path
import json

# PDF reading
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  pdfplumber not installed. PDF reading disabled. Install: pip install pdfplumber")

# DOCX reading
try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("⚠️  python-docx not installed. DOCX reading disabled. Install: pip install python-docx")

# Image OCR
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR not available. Install: pip install pillow pytesseract")


# ============================================================================
# WEBSITE SCRAPING
# ============================================================================

def scrape_website(url: str) -> dict:
    # Import sanitizer from webapp (or redefine here if needed)
    try:
        from agentspace_webapp import sanitize_unicode
    except ImportError:
        def sanitize_unicode(obj):
            if isinstance(obj, str):
                return obj.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            elif isinstance(obj, dict):
                return {sanitize_unicode(k): sanitize_unicode(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_unicode(i) for i in obj]
            elif isinstance(obj, tuple):
                return tuple(sanitize_unicode(i) for i in obj)
            elif isinstance(obj, set):
                return {sanitize_unicode(i) for i in obj}
            elif obj is None or isinstance(obj, (int, float, bool)):
                return obj
            else:
                return sanitize_unicode(str(obj))
    """
    Scrape a website and extract key business information.
    
    Args:
        url: Company website URL
    Returns:
        Dictionary with extracted information
    """
    
    print(f"🌐 Scraping website: {url}")
    
    result = {
        "url": url,
        "company_name": "",
        "tagline": "",
        "about": "",
        "mission": "",
        "services": [],
        "values": [],
        "team_info": "",
        "contact_info": {},
        "meta_description": "",
        "error": None
    }
    
    try:
        # Fetch the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        if soup.title:
            result["company_name"] = soup.title.string.strip()

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            result["meta_description"] = meta_desc.get('content', '')

        # Find sections
        result["about"] = find_section(soup, ['about', 'who we are', 'our story'])
        result["mission"] = find_section(soup, ['mission', 'vision', 'our mission'])
        result["services"] = find_services(soup)
        result["values"] = find_values(soup)
        result["team_info"] = find_section(soup, ['team', 'our team', 'leadership'])

        # Extract tagline (first H2 or prominent text)
        h2 = soup.find('h2')
        if h2:
            result["tagline"] = h2.get_text().strip()

        # If all key fields are empty, try Selenium fallback
        if not (result["about"] or result["mission"] or result["services"] or result["values"]):
            print("  ...No meaningful content with requests/BeautifulSoup, trying Selenium fallback...")
            try:
                import chromedriver_autoinstaller
                chromedriver_autoinstaller.install()
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                import time

                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--disable-dev-shm-usage')

                driver = webdriver.Chrome(options=chrome_options)
                driver.get(url)

                # Try to handle cookie popups (common selectors)
                try:
                    # Wait for cookie popup and click accept if present
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ACEPT', 'acept'), 'accept') or contains(translate(., 'ALLOW', 'allow'), 'allow') or contains(translate(., 'GOT IT', 'got it'), 'got it') or contains(translate(., 'OK', 'ok'), 'ok') or contains(translate(., 'AGREE', 'agree'), 'agree') or contains(translate(., 'CONSENT', 'consent'), 'consent')]"))
                    ).click()
                    print("  ✓ Cookie popup accepted")
                except Exception:
                    pass  # No cookie popup found or could not click

                # Wait for main content (e.g., main tag or body loaded)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "main"))
                    )
                except Exception:
                    # Fallback: wait for body
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                time.sleep(1)  # Give a moment for content to settle
                page_source = driver.page_source
                driver.quit()

                soup = BeautifulSoup(page_source, 'html.parser')
                # Re-extract fields
                if soup.title:
                    result["company_name"] = soup.title.string.strip()
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    result["meta_description"] = meta_desc.get('content', '')
                result["about"] = find_section(soup, ['about', 'who we are', 'our story'])
                result["mission"] = find_section(soup, ['mission', 'vision', 'our mission'])
                result["services"] = find_services(soup)
                result["values"] = find_values(soup)
                result["team_info"] = find_section(soup, ['team', 'our team', 'leadership'])
                h2 = soup.find('h2')
                if h2:
                    result["tagline"] = h2.get_text().strip()

                if not (result["about"] or result["mission"] or result["services"] or result["values"]):
                    # Fallback: extract all visible text for manual review
                    def get_visible_text(soup):
                        for script in soup(["script", "style", "nav", "footer", "head", "title", "meta"]):
                            script.decompose()
                        text = soup.get_text(separator=' ', strip=True)
                        return text

                    visible_text = get_visible_text(soup)
                    result["visible_text_fallback"] = visible_text[:10000]  # Limit to 10k chars
                    result["error"] = "No meaningful structured content extracted, but all visible text is included for manual review."
                    print(f"  ✗ Error: {result['error']} (visible text fallback provided)")
                else:
                    print(f"  ✓ Extracted (Selenium): {len(result['about'])} chars about, {len(result['services'])} services")
            except Exception as se:
                result["error"] = f"Selenium fallback failed: {str(se)}"
                print(f"  ✗ Error: {result['error']}")
        else:
            print(f"  ✓ Extracted: {len(result['about'])} chars about, {len(result['services'])} services")

    except requests.RequestException as e:
        result["error"] = f"Failed to fetch website: {str(e)}"
        print(f"  ✗ Error: {result['error']}")

    except Exception as e:
        result["error"] = f"Error parsing website: {str(e)}"
        print(f"  ✗ Error: {result['error']}")

    # Sanitize all extracted fields before returning
    return sanitize_unicode(result)


def extract_main_text(soup) -> str:
    """Extract main text content from page."""
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text


def find_section(soup, keywords: list) -> str:
    """Find a section by keywords in headings."""
    for keyword in keywords:
        # Look for headings with this keyword
        for tag in ['h1', 'h2', 'h3', 'h4']:
            headings = soup.find_all(tag, string=re.compile(keyword, re.IGNORECASE))
            for heading in headings:
                # Get the next few paragraphs
                content = []
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['p', 'div']:
                        content.append(sibling.get_text().strip())
                    if len(content) >= 3:  # Get first 3 paragraphs
                        break
                if content:
                    return ' '.join(content)[:500]  # Limit to 500 chars
    return ""


def find_services(soup) -> list:
    """Extract list of services/products."""
    services = []
    
    # Look for common service section patterns
    service_keywords = ['services', 'products', 'solutions', 'what we do', 'offerings']
    
    for keyword in service_keywords:
        # Find section heading
        section = soup.find(['h2', 'h3'], string=re.compile(keyword, re.IGNORECASE))
        if section:
            # Look for list items
            ul = section.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    service_text = li.get_text().strip()
                    if service_text and len(service_text) < 100:
                        services.append(service_text)
            
            # Or look for h4 headings
            for h in section.find_next_siblings(['h4', 'h5']):
                service_text = h.get_text().strip()
                if service_text and len(service_text) < 100:
                    services.append(service_text)
                if len(services) >= 6:
                    break
    
    return services[:10]  # Limit to 10


def find_values(soup) -> list:
    """Extract company values."""
    values = []
    
    keywords = ['values', 'core values', 'our values', 'principles']
    
    for keyword in keywords:
        section = soup.find(['h2', 'h3'], string=re.compile(keyword, re.IGNORECASE))
        if section:
            # Look for list
            ul = section.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    value_text = li.get_text().strip()
                    # Extract just the value name (before colon or dash)
                    value_name = value_text.split(':')[0].split('-')[0].strip()
                    if value_name and len(value_name) < 50:
                        values.append(value_name)
    
    return values[:8]  # Limit to 8


# ============================================================================
# FILE ANALYSIS
# ============================================================================

def analyze_uploaded_file(filepath: str) -> dict:
    """
    Analyze an uploaded file and extract information.
    
    Args:
        filepath: Path to uploaded file
        
    Returns:
        Dictionary with extracted information
    """
    
    filepath = Path(filepath)
    print(f"📄 Analyzing file: {filepath.name}")
    
    result = {
        "filename": filepath.name,
        "file_type": filepath.suffix.lower(),
        "content": "",
        "metadata": {},
        "error": None
    }
    
    try:
        if filepath.suffix.lower() == '.pdf':
            result["content"] = extract_pdf_text(filepath)
            result["metadata"] = extract_pdf_metadata(filepath)
        
        elif filepath.suffix.lower() in ['.docx', '.doc']:
            result["content"] = extract_docx_text(filepath)
        
        elif filepath.suffix.lower() in ['.txt', '.md']:
            result["content"] = filepath.read_text(encoding='utf-8')
        
        elif filepath.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            result["content"] = extract_image_text(filepath)
        
        else:
            result["error"] = f"Unsupported file type: {filepath.suffix}"
        
        if not result["content"] or len(result["content"].strip()) < 50:
            result["error"] = f"No meaningful content extracted from file: {filepath.name}"
            print(f"  ✗ Error: {result['error']}")
        else:
            print(f"  ✓ Extracted {len(result['content'])} characters")
        
    except Exception as e:
        result["error"] = f"Error reading file: {str(e)}"
        print(f"  ✗ Error: {result['error']}")
    
    return result


def extract_pdf_text(filepath: Path) -> str:
    """Extract text from PDF."""
    if not PDF_AVAILABLE:
        return "[PDF reading not available - install pdfplumber]"
    
    text = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages[:20]:  # Limit to first 20 pages
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        return f"[Error reading PDF: {str(e)}]"
    
    return '\n\n'.join(text)


def extract_pdf_metadata(filepath: Path) -> dict:
    """Extract PDF metadata."""
    if not PDF_AVAILABLE:
        return {}
    
    metadata = {}
    try:
        with pdfplumber.open(filepath) as pdf:
            if pdf.metadata:
                metadata = {
                    'title': pdf.metadata.get('Title', ''),
                    'author': pdf.metadata.get('Author', ''),
                    'subject': pdf.metadata.get('Subject', ''),
                    'pages': len(pdf.pages)
                }
    except:
        pass
    
    return metadata


def extract_docx_text(filepath: Path) -> str:
    """Extract text from DOCX."""
    if not DOCX_AVAILABLE:
        return "[DOCX reading not available - install python-docx]"
    
    try:
        doc = DocxDocument(filepath)
        text = []
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
        return '\n\n'.join(text)
    except Exception as e:
        return f"[Error reading DOCX: {str(e)}]"


def extract_image_text(filepath: Path) -> str:
    """Extract text from image using OCR."""
    if not OCR_AVAILABLE:
        return "[OCR not available - install pillow and pytesseract]"
    
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"[Error extracting text from image: {str(e)}]"


# ============================================================================
# DATA SYNTHESIS
# ============================================================================

def synthesize_data(website_data: dict, file_data: list, form_data: dict) -> dict:
    """
    Combine website scraping, file analysis, and form data into complete profile.
    
    Args:
        website_data: Data from website scraping
        file_data: List of analyzed files
        form_data: Data from web form
        
    Returns:
        Complete, enriched company profile
    """
    
    print("🔄 Synthesizing all data sources...")
    
    # Start with form data
    profile = form_data.copy()


    # Enrich from website
    if website_data:
        about_text = website_data.get('about', '')
        used_fallback = False
        fallback_text = website_data.get('visible_text_fallback', '')
        # Filter out cookie consent, navigation, testimonials, and irrelevant lines from fallback text
        if fallback_text:
            lines = fallback_text.splitlines()
            filtered_lines = [line for line in lines if not re.search(r'cookie|consent|shopify|ads|analytics|privacy|agree|accept|cart|login|facebook|instagram|twitter|testimonials|review|quote|buy|checkout|continue shopping|return envelope|digital results|kit|sample|hair|mail|register|id|doctor|vet|panel|medical|advisory|usa|lab|non-invasive|needle|skin prick|waiting room|co-pay|cost|meet|team|contact|address|phone|email|open window|refresh|page|sunscreen|shampoo|detergent|soap|lotion|mineral|vitamin|amino acid|fatty acid|metal|pollens|grass|plants|chemicals|pet|dog|cat|furry|friends|children|kids|seniors|shopping list|nutrition expert|resource|one time test|repeat customer|first time customer|success|revenue|metrics|belief|outcome|collaborator|partner|vendor|amazon|pet supply|store|unique|valuable|retailer|b2c|tool|loyalty|sales|transformation|customer|feedback|surprise|best|normal|better|option|aha|moment|essential|protein|carnivore|diet|overload|screening|timezone|america|new york|gmt', line, re.IGNORECASE)]
            fallback_text = '\n'.join(filtered_lines)

        # Improved keyword and section-based extraction for business fields
        def extract_section(text, section_keywords, maxlen=400):
            # Try to find section by heading
            for kw in section_keywords:
                pattern = rf'(?:^|\n)\s*{kw}[:\-]?\s*(.+?)(?:\n\s*[A-Z][a-z ]{{2,20}}[:\-]|\n\s*$|\n\s*[A-Z][a-z ]{{2,20}}$)'
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    return match.group(1).strip()[:maxlen]
            # Fallback: keyword-based extraction
            for kw in section_keywords:
                match = re.search(rf'{kw}[^.\n]{{0,100}}[:\-]?\s*([^.\n]{{10,{maxlen}}})[.\n]', text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            return ''


        # Company Overview
        # If about_text and overview are weak, merge file_content
        def is_weak(text):
            return not text or len(text.strip()) < 100 or re.search(r'(cookie|consent|testimonial|review|quote|cart|login|shopify|buy|checkout|continue shopping|return envelope|kit|sample|hair|mail|register|id|doctor|vet|panel|medical|advisory|usa|lab|non-invasive|needle|skin prick|waiting room|co-pay|cost|meet|team|contact|address|phone|email|open window|refresh|page|sunscreen|shampoo|detergent|soap|lotion|mineral|vitamin|amino acid|fatty acid|metal|pollens|grass|plants|chemicals|pet|dog|cat|furry|friends|children|kids|seniors|shopping list|nutrition expert|resource|one time test|repeat customer|first time customer|success|revenue|metrics|belief|outcome|collaborator|partner|vendor|amazon|pet supply|store|unique|valuable|retailer|b2c|tool|loyalty|sales|transformation|customer|feedback|surprise|best|normal|better|option|aha|moment|essential|protein|carnivore|diet|overload|screening|timezone|america|new york|gmt)', text, re.IGNORECASE)

        file_content = ''
        if file_data:
            all_file_text = [f.get('content','') for f in file_data if f.get('content')]
            file_content = '\n'.join(all_file_text)

        if not about_text and fallback_text:
            about_text = extract_section(fallback_text, ['about', 'who we are', 'our story', 'brand story', 'company overview', 'overview', 'what we do', 'what is', 'introduction'], 2000)
            if not about_text:
                about_text = fallback_text[:2000]
            used_fallback = True
        profile['company_name'] = profile.get('company_name') or website_data.get('company_name', '')

        overview = ''
        if not profile.get('company_overview') and fallback_text:
            overview = extract_section(fallback_text, ['about', 'who we are', 'our story', 'brand story', 'company overview', 'overview', 'what we do', 'what is', 'introduction'], 2000)
        overview = overview or about_text
        # If overview is weak, merge file_content
        if is_weak(overview) and file_content:
            overview = (overview + '\n' + file_content[:1500]).strip()
        profile['company_overview'] = profile.get('company_overview') or overview

        # Mission Statement
        mission = profile.get('mission_statement') or website_data.get('mission', '')
        if not mission and fallback_text:
            mission = extract_section(fallback_text, ['mission', 'vision', 'purpose', 'why we exist', 'our mission', 'goal', 'objective', 'aim', 'philosophy'], 400)
            if not mission:
                mission = fallback_text[:400]
        # If mission is weak, merge file_content
        if is_weak(mission) and file_content:
            mission = (mission + '\n' + file_content[:500]).strip()
        profile['mission_statement'] = mission

        # Tagline
        if not profile.get('tagline'):
            tagline = website_data.get('tagline', '')
            if not tagline and fallback_text:
                tagline = extract_section(fallback_text, ['tagline', 'slogan', 'promise', 'brand promise', 'motto', 'catchphrase', 'one-liner'], 100)
                # Skip irrelevant headings
                tagline_lines = [line for line in fallback_text.split('\n') if not re.search(r'cookie|consent|privacy|shopify|cart|login|facebook|instagram|twitter|accept|decline|skip|continue|checkout|buy|kit|sample|mail|register|id|doctor|vet|panel|medical|advisory|usa|lab|non-invasive|needle|skin prick|waiting room|co-pay|cost|meet|team|contact|address|phone|email|open window|refresh|page', line, re.IGNORECASE)]
                if not tagline and tagline_lines:
                    tagline = tagline_lines[0][:100]
            # If still not found, fallback to meta_description
            if not tagline:
                tagline = website_data.get('meta_description', '')[:100]
            profile['tagline'] = tagline

        # Services/Products
        services = website_data.get('services', [])
        if not services and fallback_text:
            service_lines = re.findall(r"(?:services|products|offerings|solutions|what we offer|what we provide|test for|tests for|screen for|help with|features|capabilities|specialties|areas)[:\-]?\s*([^.\n]{5,100})", fallback_text, re.IGNORECASE)
            services = [s.strip() for s in service_lines if not re.search(r'cookie|privacy|consent|shopify|ads|analytics', s, re.IGNORECASE)]
        if services:
            existing_services = profile.get('products_services', [])
            if isinstance(existing_services, str):
                existing_services = [s.strip() for s in existing_services.split(',')]
            profile['products_services'] = list(set(existing_services + services))[:10]

        # Values
        values = website_data.get('values', [])
        if not values and fallback_text:
            value_lines = re.findall(r"(?:values|principles|pillars|beliefs|core beliefs|guiding beliefs|culture|ethos|what we stand for|what matters|what guides us|what we never compromise)[:\-]?\s*([^.\n]{5,100})", fallback_text, re.IGNORECASE)
            values = [v.strip() for v in value_lines if not re.search(r'cookie|privacy|consent|shopify|ads|analytics', v, re.IGNORECASE)]
        if values:
            existing_values = profile.get('core_values', [])
            if isinstance(existing_values, str):
                existing_values = [v.strip() for v in existing_values.split(',')]
            profile['core_values'] = list(set(existing_values + values))[:8]

        # Team Info
        team_info = website_data.get('team_info', '')
        if not team_info and fallback_text:
            team_info = extract_section(fallback_text, ['team', 'leadership', 'our team', 'meet the team', 'who we are', 'panel', 'advisory panel', 'medical panel'], 400)
        if team_info:
            profile['team_info'] = team_info

        # Contact Info
        contact_info = website_data.get('contact_info', {})
        if not contact_info and fallback_text:
            # Try to extract email, phone, address
            email_match = re.search(r'([\w\.-]+@[\w\.-]+)', fallback_text)
            phone_match = re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', fallback_text)
            address_match = re.search(r'(\d{1,5} [A-Za-z0-9 .,-]+,? [A-Za-z ]+,? [A-Za-z]{2,} \d{5})', fallback_text)
            contact_info = {}
            if email_match:
                contact_info['email'] = email_match.group(1)
            if phone_match:
                contact_info['phone'] = phone_match.group(1)
            if address_match:
                contact_info['address'] = address_match.group(1)
        if contact_info:
            profile['contact_info'] = contact_info

    # Enrich from files
    if file_data:
        # Combine all file content
        all_file_text = []
        for file_info in file_data:
            if file_info.get('error'):
                profile.setdefault('file_errors', []).append(file_info['error'])
            elif file_info.get('content'):
                all_file_text.append(file_info['content'])

        combined_files = '\n\n'.join(all_file_text)
        # Store raw file content for reference
        if combined_files:
            profile['file_content'] = combined_files[:5000]  # First 5000 chars

    # Only set error if neither structured nor fallback content is present
    if (
        (website_data and website_data.get('error')) or
        (file_data and all(f.get('error') for f in file_data)) or
        (not profile.get('company_overview') and not profile.get('mission_statement') and not profile.get('products_services'))
    ):
        # If fallback was used for company_overview, do NOT set error
        if not used_fallback:
            profile['error'] = profile.get('error') or 'No meaningful data extracted from website or files.'
            print(f"  ✗ Synthesis error: {profile.get('error')}")
        else:
            profile.pop('error', None)
            print(f"  ✓ Synthesized profile for: {profile.get('company_name', 'Unknown')} (fallback used)")
    else:
        print(f"  ✓ Synthesized profile for: {profile.get('company_name', 'Unknown')}")

    return profile


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def analyze_all_sources(website_url: str, uploaded_files: list, form_data: dict) -> dict:
    """
    One-stop function to analyze all data sources.
    
    Args:
        website_url: Client website URL
        uploaded_files: List of file paths
        form_data: Data from web form
        
    Returns:
        Complete enriched profile
    """
    
    print("=" * 80)
    print("ANALYZING ALL DATA SOURCES")
    print("=" * 80)
    print()
    
    # Scrape website
    website_data = {}
    if website_url:
        website_data = scrape_website(website_url)
        print("--- Website Data Extracted ---")
        print(json.dumps(website_data, indent=2, ensure_ascii=False))
    else:
        print("⚠️  No website URL provided")

    print()

    # Analyze files
    file_data = []
    if uploaded_files:
        print(f"📁 Analyzing {len(uploaded_files)} uploaded file(s)...")
        for filepath in uploaded_files:
            file_info = analyze_uploaded_file(filepath)
            file_data.append(file_info)
        print("--- File Data Extracted ---")
        print(json.dumps(file_data, indent=2, ensure_ascii=False))
        print()
    else:
        print("⚠️  No files uploaded")
        print()

    # Synthesize
    enriched_profile = synthesize_data(website_data, file_data, form_data)

    print("--- Final Synthesized Profile ---")
    print(json.dumps(enriched_profile, indent=2, ensure_ascii=False))
    print("=" * 80)
    print("DATA ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    return enriched_profile


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    # Test scraping
    print("Testing web scraper...")
    test_url = "https://www.anthropic.com"
    result = scrape_website(test_url)
    print(json.dumps(result, indent=2))
