import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Load environment variables from backend/.env
env_file = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(env_file)

from models.job import Job

# ----------------------------
# Database setup
# ----------------------------
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print(" No DATABASE_URL found in environment variables")
    sys.exit(1)

print(f"🔗 Connecting to database: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


# ----------------------------
# Scraper setup
# ----------------------------
def clean_location_text(location):
    """Clean location text by removing emojis and salary information"""
    if not location:
        return location
    
    import re
    
    # Remove emojis and special characters
    cleaned = re.sub(r'[^\w\s\-.,()]', '', location)
    
    # Remove salary-related patterns
    salary_patterns = [
        r'\$[\d,]+(?:-\$[\d,]+)?',  # $50k-$100k
        r'💰\s*\$[\d,]+(?:-\$[\d,]+)?',  # 💰 $50k-$100k
        r'[\d,]+k-[\d,]+k',  # 50k-100k
        r'[\d,]+k\+',  # 50k+
        r'£[\d,]+(?:-£[\d,]+)?',  # £50k-£100k
        r'[\d,]+-[\d,]+',  # 50-100
    ]
    
    for pattern in salary_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    # Handle specific cases
    if cleaned.lower() in ['usa', 'us', 'united states']:
        cleaned = 'USA'
    elif cleaned.lower() in ['uk', 'united kingdom']:
        cleaned = 'UK'
    elif cleaned.lower() in ['remote', 'work from home', 'wfh']:
        cleaned = 'Remote'
    
    return cleaned

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrape_jobs():
    driver = get_driver()
    base_url = "https://www.actuarylist.com/"
    driver.get(base_url)

    time.sleep(3)  # wait for page to load fully

    jobs_added = 0
    current_page = 1
    max_pages = 10  # Limit  pages maximum

    while current_page <= max_pages:
        print(f" Scraping page {current_page}/{max_pages}")
        
        # Look for job cards - they appear to be individual job listings
        # More specific selectors to avoid page headers and navigation
        job_cards = driver.find_elements(By.CSS_SELECTOR, 
            "div:has(img[src*='logo']):has(h2, h3, h4), " +
            "div:has(img[src*='logo']):has([class*='title']), " +
            "div:has(img[src*='logo']):has(strong), " +
            "[class*='job-card'], " +
            "[class*='job-listing'], " +
            "article:has(img[src*='logo'])"
        )
        
        if not job_cards:
            print(" No job elements found on this page.")
            # Try alternative selectors for job-specific content
            job_cards = driver.find_elements(By.CSS_SELECTOR, 
                "div:has(img[src*='logo']):has(text), " +
                "div:has([class*='company']):has([class*='title']), " +
                "div:has([class*='employer']):has([class*='position'])"
            )
            
        if not job_cards:
            print(" Still no job elements found. Trying to get page source...")
            page_source = driver.page_source[:2000]
            print(f"Page source preview: {page_source}")
            print(" No valid job elements found on this page. Moving to next page or stopping.")
            # Try to move to next page instead of breaking
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(text(),'Next') or contains(text(),'›') or contains(text(),'→')]")
                if next_button:
                    print(" Clicking next page...")
                    next_button.click()
                    time.sleep(3)
                    current_page += 1
                    continue
                else:
                    print(" No next page button found. Stopping.")
                    break
            except NoSuchElementException:
                # Try URL-based pagination
                try:
                    next_url = base_url + f"?page={current_page + 1}"
                    print(f" Trying direct URL navigation: {next_url}")
                    driver.get(next_url)
                    time.sleep(3)
                    current_page += 1
                except Exception as e:
                    print(f" Could not navigate to next page: {e}")
                    break

        print(f" Found {len(job_cards)} potential job elements on this page.")

        for card in job_cards:
            try:
                # Skip if card is too small (likely not a job)
                if len(card.text.strip()) < 50:
                    continue
                    
                # Skip if card contains navigation or page elements
                card_text_lower = card.text.lower()
                if any(x in card_text_lower for x in [
                    'find handpicked actuarial jobs',
                    'filters',
                    'search jobs',
                    'about',
                    'blog',
                    'country',
                    'city',
                    'experience',
                    'sector',
                    'tags',
                    'showing',
                    'next',
                    'previous'
                ]):
                    continue

                # Job Title - look for headings
                job_title = "Unknown Title"
                try:
                    title_el = card.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, [class*='title'], strong")
                    job_title = title_el.text.strip()
                except NoSuchElementException:
                    # Fallback: look for first meaningful line
                    lines = [line.strip() for line in card.text.split('\n') if line.strip()]
                    for line in lines:
                        if len(line) > 5 and not any(x in line.lower() for x in ['logo', 'featured', 'apply', 'ago']):
                            job_title = line
                    break

                # Company - look for company name near logo or in text
                company = "Unknown Company"
                try:
                    # Look for company logo alt text or nearby text
                    logo_el = card.find_element(By.CSS_SELECTOR, "img[src*='logo'], img[alt*='logo']")
                    company = logo_el.get_attribute("alt") or logo_el.get_attribute("title") or "Unknown Company"
                except NoSuchElementException:
                    # Look for company text
                    try:
                        company_el = card.find_element(By.CSS_SELECTOR, "[class*='company'], [class*='employer']")
                        company = company_el.text.strip()
                    except NoSuchElementException:
                        # Fallback: look for company-like text
                        lines = [line.strip() for line in card.text.split('\n') if line.strip()]
                        for line in lines:
                            if (line != job_title and len(line) > 2 and 
                                not any(x in line.lower() for x in ['remote', 'posted', 'apply', 'ago', 'featured', '💰', '🇺🇸', '🇬🇧'])):
                                company = line
                    break

                # Skip if we don't have essential info
                if job_title == "Unknown Title" or company == "Unknown Company":
                    continue

                # Skip if title is too generic or too long (likely not a real job)
                if (len(job_title) < 5 or 
                    len(job_title) > 150 or
                    job_title.count(' ') < 1 or
                    job_title.count(' ') > 12):
                    print(f" Skipping generic title: {job_title}")
                    continue

                # Skip if company name is too generic
                if (len(company) < 2 or 
                    len(company) > 80 or
                    company.lower() in ['logo', 'filters', 'filter', 'search', 'about', 'filters']):
                    print(f" Skipping generic company: {company}")
                    continue

                # Skip if job title is actually a company name (common mistake)
                company_names = [
                    'guardian life', 'swiss re', 'hannover re', 'liberty mutual', 
                    'munich re', 'state farm', 'metlife', 'travelers', 'deloitte',
                    'aig', 'wtw', 'scor', 'qbe', 'bupa', 'kpmg', 'isio', 'legal & general'
                ]
                if job_title.lower() in company_names:
                    print(f" Skipping company name as job title: {job_title}")
                    continue

                # Skip if job title is a location (country/city)
                if any(x in job_title for x in ['🇺🇸', '🇬🇧', '🇮🇳', '🇨🇦', '🇩🇪', '🇸🇬', '🇦🇺', 'USA', 'UK', 'Canada']):
                    print(f" Skipping location as job title: {job_title}")
                    continue

                # Skip if job title is a page element
                page_elements = ['filters', 'filter', 'find handpicked actuarial jobs', 'search jobs']
                if any(element in job_title.lower() for element in page_elements):
                    print(f" Skipping page element as job title: {job_title}")
                    continue

                # Location - look for location indicators
                location = "Remote"  # Default
                try:
                    # Look for country flags and location text
                    location_el = card.find_element(By.CSS_SELECTOR, "[class*='location'], [class*='place']")
                    location = clean_location_text(location_el.text.strip())
                except NoSuchElementException:
                    # Look for country flags and city names
                    try:
                        # Look for text that might be location
                        lines = [line.strip() for line in card.text.split('\n') if line.strip()]
                        for line in lines:
                            if any(x in line for x in ['🇺🇸', '🇬🇧', '🇮🇳', '🇨🇦', '🇩🇪', '🇸🇬', '🇦🇺']) or \
                               any(x in line for x in ['NY', 'MA', 'IL', 'TX', 'CA', 'London', 'Manchester', 'Toronto']):
                                location = clean_location_text(line)
                    except:
                        pass

                
                # Description
                # ----------------------------
                try:
                    description = card.find_element(By.CSS_SELECTOR, ".description, p").text.strip()
                except NoSuchElementException:
                    description = ""

                # ----------------------------
                # Job Type - determine from title and text
                # ----------------------------
                job_type = "Full-time"  # Default
                text_lower = card.text.lower()
                if "intern" in text_lower:
                    job_type = "Intern"
                elif "part-time" in text_lower or "part time" in text_lower:
                    job_type = "Part-time"
                elif "contract" in text_lower:
                    job_type = "Contract"

                # ----------------------------
                # Experience Level - determine from title and text
                # ----------------------------
                experience_level = "Not Specified"
                if any(word in text_lower for word in ["senior", "sr", "lead", "director", "vp"]):
                    experience_level = "Senior Level"
                elif any(word in text_lower for word in ["associate", "mid", "experienced"]):
                    experience_level = "Mid Level"
                elif any(word in text_lower for word in ["junior", "entry", "graduate", "intern"]):
                    experience_level = "Entry Level"

                # ----------------------------
                # Tags - extract from the job card
                # ----------------------------
                tags = []
                try:
                    # Look for tag elements
                    tag_elements = card.find_elements(By.CSS_SELECTOR, "[class*='tag'], .tags span, [class*='skill']")
                    tags = [t.text.strip() for t in tag_elements if t.text.strip()]
                    
                    # If no explicit tags, extract keywords from text
                    if not tags:
                        text_lower = card.text.lower()
                        keywords = [
                            "health", "life", "pricing", "modelling", "modeling", "p&c",
                            "property", "casualty", "python", "r", "sql", "sas", "data science",
                            "machine learning", "risk", "pension", "retirement", "analytics",
                            "fellow", "associate", "analyst", "actuary", "senior", "manager",
                            "excel", "vba", "power bi", "tableau", "alteryx", "prophet", "axis"
                        ]
                        for keyword in keywords:
                            if keyword in text_lower:
                                tags.append(keyword.title())
                except NoSuchElementException:
                    pass

                # ----------------------------
                # Salary Range - look for salary indicators
                # ----------------------------
                salary_range = "Not Specified"
                try:
                    salary_el = card.find_element(By.XPATH, ".//*[contains(text(),'$') or contains(text(),'£') or contains(text(),'💰')]")
                    salary_text = salary_el.text.strip()
                    if any(x in salary_text for x in ['$', '£', '💰']):
                        salary_range = salary_text
                except NoSuchElementException:
                    pass

                # ----------------------------
                # Posting Date - default to current time
                # ----------------------------
                posting_date = datetime.utcnow()

                # ----------------------------
                # Duplicate Check
                # ----------------------------
                # Check for duplicates based on title and company
                existing_job = session.query(Job).filter(
                    Job.title == job_title,
                    Job.company == company
                ).first()

                if existing_job:
                    print(f"⏭️ Skipping duplicate: {job_title} at {company}")
                    continue

                # ----------------------------
                # Save Job
                # ----------------------------
                job = Job(
                    title=job_title,
                    company=company,
                    location=location,
                    posting_date=posting_date,
                    job_type=job_type,
                    tags=", ".join(tags) if tags else "Not Specified",
                    salary_range=salary_range,
                    experience_level=experience_level,
                    description=description
                )
                session.add(job)
                session.commit()
                jobs_added += 1
                print(f" Added: {job_title} at {company}")

            except Exception as e:
                print(f" Error parsing job card: {e}")
                continue

        print(f" Saved {jobs_added} jobs so far.")

        # Check if we've reached the page limit
        if current_page >= max_pages:
            print(f" Reached maximum page limit ({max_pages}). Stopping scraper.")
            break

        # Next page button - look for pagination
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(text(),'Next') or contains(text(),'›') or contains(text(),'→')]")
            if next_button:
                print(" Clicking next page...")
                next_button.click()
                time.sleep(3)
                current_page += 1
            else:
                print(" No next page button found. Stopping.")
                break
        except NoSuchElementException:
            # Try URL-based pagination
            try:
                next_url = base_url + f"?page={current_page + 1}"
                print(f" Trying direct URL navigation: {next_url}")
                driver.get(next_url)
                time.sleep(3)
                current_page += 1
            except Exception as e:
                print(f" Could not navigate to next page: {e}")
                break

    print(f" Scraping completed. Total jobs scraped: {jobs_added} from {current_page} pages.")
    driver.quit()
    session.close()


if __name__ == "__main__":
    print(" Starting ActuaryList Job Scraper...")
    scrape_jobs()
    print("✨ Scraping completed!")
