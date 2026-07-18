import json
from multiprocessing import context
import time
from datetime import datetime
from playwright.sync_api import sync_playwright


# SHAHID'S LINKEDIN JOB FINDER AGENT


JOB_KEYWORDS = [
    "Data Analyst Fresher",
    "Data Scientist Fresher",
    "Junior Data Analyst",
    "Business Analyst Fresher"
]

LOCATIONS = ["Hyderabad", "Bangalore", "India"]

def search_linkedin_jobs(page, keyword, location):
    """Search jobs on LinkedIn"""
    jobs = []
    
    try:
        keyword_encoded = keyword.replace(' ', '%20')
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword_encoded}&location={location}&f_E=1%2C2&sortBy=DD"
        
        print(f"\n🔍 Searching: '{keyword}' in {location}")
        page.goto(url, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)
        
        # Scroll to load jobs
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
        
        # Try multiple selectors
        selectors = [
            'li.jobs-search-results__list-item',
            'ul.jobs-search__results-list li',
            'div.job-search-card',
            'div.base-card',
            '.scaffold-layout__list li',
            'li[data-occludable-job-id]',
            'div[data-job-id]'
        ]
        
        job_cards = []
        for selector in selectors:
            job_cards = page.query_selector_all(selector)
            if job_cards:
                print(f"  Using selector: {selector}")
                print(f"  Found {len(job_cards)} jobs")
                break
        
        if not job_cards:
            # Take screenshot to debug
            page.screenshot(path=f"debug_{keyword[:10]}.png")
            print(f"   No jobs found — screenshot saved!")
            return jobs
        
        for card in job_cards[:8]:
            try:
                # Try multiple title selectors
                title = None
                for sel in [
                    'h3.base-search-card__title',
                    'a.job-card-list__title',
                    'h3',
                    'a[data-control-name="jobcard_title"]',
                    '.job-card-container__link'
                ]:
                    elem = card.query_selector(sel)
                    if elem:
                        title = elem.inner_text().strip()
                        if title:
                            break
                
                if not title:
                    continue
                

                # Company
                company = None
                for sel in [
                    '.job-card-container__company-name',
                    'h4.base-search-card__subtitle', 
                    '.artdeco-entity-lockup__subtitle',
                    'span.job-card-container__primary-description',
                    'h4'
                ]:
                    elem = card.query_selector(sel)
                    if elem:
                        company = elem.inner_text().strip()
                        if company:
                            break
                company = company or "N/A"
                
                # Location
                loc_elem = card.query_selector(
                    'span.job-search-card__location, .job-card-container__metadata-item, span'
                )
                job_location = loc_elem.inner_text().strip() if loc_elem else location
                
                # Link
                link_elem = card.query_selector('a')
                link = link_elem.get_attribute('href') if link_elem else "N/A"
                if link:
                    if link.startswith('/'):
                        link = 'https://www.linkedin.com' + link
                    if '?' in link:
                        link = link.split('?')[0]
                
                # Posted
                time_elem = card.query_selector('time')
                posted = time_elem.inner_text().strip() if time_elem else "Recent"
                
                if title and len(title) > 3:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'posted': posted,
                        'link': link,
                        'keyword': keyword
                    })
                    print(f"  ✅ {title} — {company}")
                    
            except:
                continue
                
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return jobs

def filter_jobs(jobs):
    """Filter relevant jobs"""
    avoid_keywords = [
        'senior', 'manager', 'director', 'lead',
        'head', '5+ years', '7+ years', '10+ years'
    ]
    
    filtered = []
    seen = set()
    
    for job in jobs:
        text = (job['title'] + ' ' + job['company']).lower()
        
        if any(kw in text for kw in avoid_keywords):
            continue
        
        key = f"{job['title']}_{job['company']}"
        if key not in seen:
            seen.add(key)
            filtered.append(job)
    
    return filtered

def generate_report(jobs):
    """Generate WhatsApp report"""
    now = datetime.now().strftime('%d %b %Y, %I:%M %p')
    
    report = f" *Shahid's Job Finder*\n"
    report += f" {now}\n"
    report += f"{'='*35}\n\n"
    report += f" *{len(jobs)} Jobs Found!*\n\n"
    
    for i, job in enumerate(jobs[:15], 1):
        clean_title = job['title'].split('\n')[0].strip()
        report += f"*{i}. {clean_title}*\n"
        report += f" {job['company']}\n"
        clean_loc = job['location'].split('\n')[0].strip()
        report += f"📍 {clean_loc}\n"
        report += f" {job['posted']}\n"
        report += f" {job['link']}\n\n"
    
    report += f" *Apply cheyyi Shahid!* \n"
    
    with open('job_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    with open('jobs_found.json', 'w', encoding='utf-8') as f:
        json.dump({'date': datetime.now().isoformat(),
                   'total': len(jobs), 'jobs': jobs},
                  f, indent=2, ensure_ascii=False)
    
    return report

def main():
    print(" SHAHID'S LINKEDIN JOB FINDER AGENT")
    print("="*50)
    
    with sync_playwright() as p:
        # Launch Brave browser
        context = p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\TheSh\AppData\Local\Playwright\BraveSession",
            executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            headless=False,
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )

        page = context.new_page()
        all_jobs = []
        
        try:
            # Check LinkedIn login
            page.goto("https://www.linkedin.com/feed/")
            page.wait_for_timeout(3000)
            
            if "login" in page.url:
                print(" Not logged in!")
                input("Login cheyyi, Enter press cheyyi...")
            else:
                print(" LinkedIn logged in!")
            
            # Search jobs
            for keyword in JOB_KEYWORDS[:2]:
                for location in LOCATIONS[:2]:
                    jobs = search_linkedin_jobs(page, keyword, location)
                    all_jobs.extend(jobs)
                    time.sleep(3)
            
            # Filter
            filtered = filter_jobs(all_jobs)
            print(f"\n {len(filtered)} relevant jobs found!")
            
            # Report
            report = generate_report(filtered)
            
            print("\n" + "="*50)
            print(" WHATSAPP REPORT:")
            print("="*50)
            print(report)
            print("\n Saved to job_report.txt!")
            
        except Exception as e:
            print(f" Error: {e}")
            
        finally:
            input("\nEnter press cheyyi to close...")
            context.close()

if __name__ == "__main__":
    main()