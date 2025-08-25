import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime
import pytz

def generate_rss():
    # URL of the income tax notifications page
    url = 'https://www.incometaxindia.gov.in/Pages/notifications.aspx'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Create RSS feed generator
        fg = FeedGenerator()
        fg.title('Income Tax India Notifications')
        fg.description('Latest Income Tax Notifications from India')
        fg.link(href='https://www.incometaxindia.gov.in/Pages/notifications.aspx', rel='alternate')
        fg.language('en')
        
        # Find notifications - adjust selectors based on actual page structure
        # This is a generic example - you may need to inspect the actual page
        notifications = soup.find_all('div', class_='notification-item') or soup.find_all('li')
        
        for i, item in enumerate(notifications[:15]):  # Limit to 15 items
            # Extract title and link - adjust based on actual structure
            link_tag = item.find('a')
            if not link_tag:
                continue
                
            title = link_tag.get_text(strip=True)
            link = link_tag.get('href', '')
            
            # Make relative URLs absolute
            if link.startswith('/'):
                link = 'https://www.incometaxindia.gov.in' + link
            
            # Create feed entry
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)
            fe.pubDate(datetime.datetime.now(pytz.utc) - datetime.timedelta(days=i))
            
        # Generate RSS feed
        fg.rss_file('rss.xml', pretty=True)
        print("RSS feed generated successfully!")
        
    except Exception as e:
        print(f"Error generating RSS feed: {e}")

if __name__ == "__main__":
    generate_rss()
