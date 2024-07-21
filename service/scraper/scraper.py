from time import sleep
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from trafilatura import extract
from db.db_connector import DbConnector
import re
import langdetect
import json
from logging import getLogger

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    start_urls = []  # This will be set dynamically

    def __init__(self, start_url, job_id, url_filter_mode, url_filter, *args, **kwargs):
        super(ScraperSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.urls = set()
        self.store = DbConnector("index", "store")
        self.filter_mode = url_filter_mode.lower()
        self.filter = url_filter
        self.job_id = job_id

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            full_url = response.urljoin(href)
            self.urls.add(full_url)
            yield scrapy.Request(full_url, callback=self.parse_page)

    def parse_page(self, response):
        self.log(f'Crawled URL: {response.url}')
        self.urls.add(response.url)
        if self.filter:
            if self.filter_mode == "inclusionary" and not re.search(self.filter, response.url):
                return
            if self.filter_mode == "exclusionary" and re.search(self.filter, response.url):
                return
        html_content = response.body.decode('utf-8')
        extracted = extract(html_content, output_format='json', with_metadata=True, favor_recall=True, include_links=True, include_formatting=True, include_contacts=True, url=response.url)
        if extracted:
            doc = json.loads(extracted)
            if self.store.collection.find_one({"fingerprint": doc['fingerprint']}):
                return
            doc['language'] = langdetect.detect(doc['raw_text'][:128])
            if doc['language'] not in ['en', 'fr', 'ru', 'uk', 'de', 'pl', 'es', 'it', 'nl']:
                return
            doc['source'] = response.url
            doc['indexed'] = False
            doc['scraper_id'] = self.job_id
            self.store.collection.insert_one(doc)

class Scraper:
    def __init__(self):
        self.jobs = DbConnector("scraper", "jobs")
        self.logger = getLogger("scraper")
        self.process = CrawlerProcess(get_project_settings())

    def log(self, message):
        self.logger.info(message)

    def spider_closed(self, spider, reason):
        # self.jobs.collection.update_one({"_id": spider.job_id}, {"$set": {"status": "done"}})
        self.log(f"Finished job: {spider.job_id} with reason: {reason}")

    def run(self):
        for job in self.jobs.collection.find():
            if "status" not in job:
                self.jobs.collection.update_one({"_id": job["_id"]}, {"$set": {"status": "pending"}})
        
        while True:
            self.log(f"Checking for pending jobs...")
            pending_jobs = list(self.jobs.collection.find({"status": "pending"}))
            if pending_jobs:
                for job in pending_jobs:
                    start_url = job["source"]
                    job_id = job["_id"]
                    url_filter_mode = job.get("pattern_mode", "inclusionary")
                    url_filter = job.get("pattern", "")
                    self.log(f"Starting job: {job_id}, URL: {start_url}")
                    crawler = self.process.create_crawler(ScraperSpider)
                    crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
                    self.process.crawl(crawler, start_url=start_url, job_id=job_id, url_filter_mode=url_filter_mode, url_filter=url_filter)
                self.process.start(stop_after_crawl=False)  # Start the crawling process
            else:
                sleep(60)  # Wait before checking for new jobs

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
