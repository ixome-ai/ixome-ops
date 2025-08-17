# /home/vincent/ixome/scrapy-selenium/control4_scraper/control4_scraper/settings.py
BOT_NAME = 'control4_scraper'

SPIDER_MODULES = ['control4_scraper.spiders']
NEWSPIDER_MODULE = 'control4_scraper.spiders'

ROBOTSTXT_OBEY = True

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

DOWNLOAD_DELAY = 5.0
DEPTH_LIMIT = 5
CONCURRENT_REQUESTS = 16

ITEM_PIPELINES = {
    'control4_scraper.pipelines.Control4ScraperPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'control4_scraper.middlewares.SeleniumMiddleware': 800,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = '/usr/local/bin/chromedriver'
SELENIUM_BROWSER_EXECUTABLE_PATH = '/opt/google/chrome/chrome'
SELENIUM_DRIVER_ARGUMENTS = ['--headless', '--disable-gpu', '--no-sandbox', '--disable-blink-features=AutomationControlled']
SELENIUM_HEADLESS = True

LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy.log'