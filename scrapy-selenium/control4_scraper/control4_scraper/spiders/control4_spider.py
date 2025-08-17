# /home/vincent/ixome/scrapy-selenium/control4_scraper/control4_scraper/spiders/control4_spider.py
# Scrapes all public Control4 PDFs from docs.control4.com, restarts chromedriver per URL, no login.
import random
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from ..items import Control4ScraperItem
from dotenv import load_dotenv
import logging
import time
from scrapy.exceptions import CloseSpider

load_dotenv(dotenv_path='/home/vincent/ixome/.env')

class Control4Spider(CrawlSpider):
    name = 'control4'
    allowed_domains = ['docs.control4.com']
    start_urls = [
        'https://docs.control4.com/docs/',
        'https://docs.control4.com/docs/product/myhome/open-source-request-form/english/latest/myhome-ios-open-source-and-object-code-request-form-rev-a.pdf',
        'https://docs.control4.com/docs/product/tunein/user-guide/latest/tunein-user-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/alexa/faq/german/latest/alexa-faq-de.pdf',
        'https://docs.control4.com/docs/product/myhome/setup-guide/latest/myhome-setup-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/networking/checklist/english/latest/network-install-checklist-rev-a.pdf',
        'https://docs.control4.com/docs/product/mycontrol4/quick-setup/latest/mycontrol4-account-quick-setup-for-consumers-rev-a.pdf',
        'https://docs.control4.com/docs/product/tunein/quick-setup/latest/tunein-quick-setup-rev-a.pdf',
        'https://docs.control4.com/docs/product/customer/brochure/english/latest/control4-comforts-brochure-rev-a.pdf',
        'https://docs.control4.com/docs/product/pakedge/brochure/english/latest/pakedge-superior-networking-brochure-rev-a.pdf',
        'https://docs.control4.com/docs/product/pcna/troubleshooting/english/latest/pcna-network-troubleshooting-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/tunein/data-sheet/latest/tunein-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/pcna/study-guide/english/latest/pcna-study-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/myhome/setup-guide/revision/C/myhome-setup-guide-rev-c.pdf',
        'https://docs.control4.com/docs/product/pcna/troubleshooting/english/revision/B/pcna-network-troubleshooting-guide-rev-b.pdf',
        'https://docs.control4.com/docs/product/wattbox/best-practices/english/latest/wattbox-best-practices-power-load-rev-a.pdf',
        'https://docs.control4.com/docs/product/triad/style-guide/english/latest/triad-style-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/alexa/dealer-faq/english/latest/alexa-dealer-faq-rev-a.pdf',
        'https://docs.control4.com/docs/product/whenthen/information-sheet/english/latest/whenthen-tips-rev-a.pdf',
        'https://docs.control4.com/docs/product/baldwin-doorlock/brochure/english/latest/baldwin-control4-brochure-rev-a.pdf',
        'https://docs.control4.com/docs/product/networking/best-practices/english/latest/networking-best-practices-rev-a.pdf',
        'https://docs.control4.com/docs/product/z2io/data-sheet/english/latest/z2io-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/pcna/pcna-faq/english/latest/pcna-faq-rev-a.pdf',
        'https://docs.control4.com/docs/product/business-tools/dealer-faq/latest/business-tools-qa-rev-a.pdf',
        'https://docs.control4.com/docs/product/vibrant-extrusions/introduction/english/latest/vibrant-extrusion-lens-end-cap-rev-a.pdf',
        'https://docs.control4.com/docs/product/pcna/troubleshooting/english/revision/E/pcna-network-troubleshooting-guide-rev-e.pdf',
        'https://docs.control4.com/docs/product/myhome/quick-setup/revision/E/myhome-setup-guide-rev-e.pdf',
        'https://docs.control4.com/docs/product/beta-test/agreement/english/latest/end-user-beta-testing-agreement-rev-a.pdf',
        'https://docs.control4.com/docs/product/myhome/quick-setup/english/latest/myhome-setup-guide-rev-a.pdf',
        'https://docs.control4.com/docs/product/z2c/data-sheet/english/latest/z2c-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/hc-250/data-sheet/english/latest/hc-250-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/hc-800/data-sheet/english/latest/hc-800-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/5-in-wall-touch-screen/data-sheet/english/latest/5-in-wall-touch-screen-data-sheet-rev-a.pdf',
        'https://docs.control4.com/docs/product/7-in-wall-touch-screen/data-sheet/english/latest/7-in-wall-touch-screen-data-sheet-rev-a.pdf',
    ]

    rules = (
        Rule(LinkExtractor(allow=('.pdf')), callback='parse_media', follow=False),
        Rule(LinkExtractor(allow=('/docs/product/', '/docs/')), follow=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_logger = logging.getLogger(__name__)
        self.custom_logger.info("Control4Spider initialized")
        self.timeout = 300  # 5-minute timeout
        self.start_time = time.time()  # Track runtime
        self.max_runtime = 7200  # 2 hours max
        self.driver = None  # Initialize driver per URL

    def start_requests(self):
        for url in self.start_urls:
            # Initialize driver for each URL
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.binary_location = '/opt/google/chrome/chrome'
            service = Service('/usr/local/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=options)
            self.custom_logger.info(f"ChromeDriver initialized for {url}")
            
            if self.load_page(url):
                yield Request(
                    url=url,
                    callback=self.parse_media if url.endswith('.pdf') else self.parse,
                    meta={'selenium_response': self.driver.page_source, 'depth': 0}
                )
            else:
                self.custom_logger.info(f"Failed to access {url}")
                safe_url = url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
                with open(f'page_source_{safe_url}.html', 'w') as f:
                    f.write(self.driver.page_source)
                self.custom_logger.info(f"Saved page source to page_source_{safe_url}.html")
            # Close driver after each URL
            try:
                self.driver.quit()
                self.custom_logger.info(f"ChromeDriver closed for {url}")
            except Exception as e:
                self.custom_logger.info(f"Error closing driver for {url}: {e}")

    def load_page(self, url):
        try:
            if time.time() - self.start_time > self.max_runtime:
                self.custom_logger.info("Max runtime reached, closing spider")
                raise CloseSpider("Max runtime reached")
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.get(url)
            time.sleep(random.uniform(15, 30))  # Delay for load
            # Accept cookie consent
            try:
                cookie_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
                )
                cookie_button.click()
                self.custom_logger.info("Accepted cookie consent")
            except Exception:
                self.custom_logger.info("No cookie consent popup")
            # Verify page loaded
            try:
                if url.endswith('.pdf'):
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'embed[type="application/pdf"]'))
                    )
                    self.custom_logger.info(f"PDF loaded successfully for {url}")
                else:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*=".pdf"], div, ul, li'))
                    )
                    self.custom_logger.info(f"Directory page loaded successfully for {url}")
            except Exception as e:
                self.custom_logger.info(f"Content not detected for {url}: {e}")
                self.driver.refresh()
                time.sleep(random.uniform(15, 30))  # Delay after refresh
            if 'LogonForm' in self.driver.current_url or 'Logoff' in self.driver.current_url or 'login' in self.driver.current_url.lower():
                self.custom_logger.info(f"Authentication required for {url}")
                return False
            return True
        except Exception as e:
            self.custom_logger.info(f"Failed to load {url}: {e}")
            safe_url = url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
            with open(f'page_source_{safe_url}.html', 'w') as f:
                f.write(self.driver.page_source)
            self.custom_logger.info(f"Saved page source to page_source_{safe_url}.html")
            return False

    def parse(self, response):
        if time.time() - self.start_time > self.max_runtime:
            self.custom_logger.info("Max runtime reached, closing spider")
            raise CloseSpider("Max runtime reached")
        if response.url.endswith('.pdf'):
            self.custom_logger.info(f"Redirected to PDF, routing to parse_media: {response.url}")
            return self.parse_media(response)
        try:
            sel = Selector(response)
        except AttributeError as e:
            self.custom_logger.info(f"Cannot parse {response.url}: {e}")
            safe_url = response.url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
            with open(f'page_source_{safe_url}.html', 'w') as f:
                f.write(self.driver.page_source)
            self.custom_logger.info(f"Saved page source to page_source_{safe_url}.html")
            return
        links = sel.css('a[href*=".pdf"]::attr(href)').getall()
        self.custom_logger.info(f"Found {len(links)} PDF links on {response.url}: {links[:5]}")
        for link in links:
            absolute_url = response.urljoin(link)
            if any(domain in absolute_url for domain in self.allowed_domains):
                # Initialize driver for each PDF
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.binary_location = '/opt/google/chrome/chrome'
                service = Service('/usr/local/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=options)
                self.custom_logger.info(f"ChromeDriver initialized for {absolute_url}")
                
                if self.load_page(absolute_url):
                    yield Request(
                        url=absolute_url,
                        callback=self.parse_media,
                        meta={'selenium_response': self.driver.page_source, 'depth': response.meta.get('depth', 0) + 1}
                    )
                else:
                    self.custom_logger.info(f"Failed to access {absolute_url}")
                    safe_url = absolute_url.replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
                    with open(f'page_source_{safe_url}.html', 'w') as f:
                        f.write(self.driver.page_source)
                    self.custom_logger.info(f"Saved page source to page_source_{safe_url}.html")
                # Close driver after each PDF
                try:
                    self.driver.quit()
                    self.custom_logger.info(f"ChromeDriver closed for {absolute_url}")
                except Exception as e:
                    self.custom_logger.info(f"Error closing driver for {absolute_url}: {e}")
        yield from super().parse(response)

    def parse_media(self, response):
        if time.time() - self.start_time > self.max_runtime:
            self.custom_logger.info("Max runtime reached, closing spider")
            raise CloseSpider("Max runtime reached")
        item = Control4ScraperItem()
        item['url'] = response.url
        item['category'] = 'PDF Document'
        item['issue'] = response.url.split('/')[-1].replace('.pdf', '')
        item['product'] = 'Control4 Core 5' if 'core-5' in response.url.lower() else 'Control4 Product'
        item['solution'] = f"PDF link for parsing: {response.url}"
        item['depth'] = response.meta.get('depth', 0)
        self.custom_logger.info(f"Yielded PDF link: {response.url} (depth {item['depth']})")
        yield item

    def closed(self, reason):
        self.custom_logger.info(f"Spider closed: {reason}")