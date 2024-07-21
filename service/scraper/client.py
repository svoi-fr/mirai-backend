import grpc

import os
import sys
gen_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gen'))
sys.path.insert(0, gen_folder)
import scraper_pb2, scraper_pb2_grpc
from config import config

class ScraperClient:
    def __init__(self, host='localhost', port=50051):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = scraper_pb2_grpc.ScraperStub(self.channel)

    def add_scraping_job(self, url, mode="recursive", country = "", source_type="", pattern_mode="", pattern = ""):
        request = scraper_pb2.ScrapingJobRequest(
            url=url,
            mode=mode.lower(),
            country=country.lower(),
            source_type=source_type.lower(),
            pattern_mode=pattern_mode,
            pattern=pattern
        )
        response = self.stub.AddScrapingJob(request)
        return response

    def close(self):
        self.channel.close()

# Example usage of the client
if __name__ == '__main__':
    client = ScraperClient(host=config.SCRAPER_HOST, port=config.SCRAPER_PORT)
    response = client.add_scraping_job(
        url="https://example.com",
        mode="full",
        country=["US", "CA"],
        source_type="html",
        pattern_mode="regex",
        pattern="<a href=\"(.+?)\">"
    )
    print("Scraping Job Response:")
    print(f"Status: {response.status}")
    print(f"Message: {response.message}")
    client.close()
