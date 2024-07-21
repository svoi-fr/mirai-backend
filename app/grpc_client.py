import os
import sys
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
gen_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../gen'))
sys.path.insert(0, root_folder)
sys.path.insert(0, gen_folder)

import grpc
from scraper_pb2 import ScrapingJobRequest, ScrapingJobResponse
from scraper_pb2_grpc import ScraperStub

from config import config

class GrpcClient:
    def __init__(self):
        pass
    
    def add_scraping_job(self, url, mode, partitions, source_type, pattern_mode, pattern):
        with grpc.insecure_channel(f'{config.SCRAPER_HOST}:{config.SCRAPER_PORT}') as channel:
            scraper = ScraperStub(channel)
            if url:
                request = ScrapingJobRequest(
                    url = url,
                    mode = mode.lower(),
                    partitions = [partition.lower() for partition in partitions],
                    source_type=source_type.lower(),
                    pattern_mode=pattern_mode.lower(),
                    pattern=pattern
                )
            else:
                print("No URL specified")
                return None
            try:
                res = scraper.AddScrapingJob(request)
                return res
            except grpc.RpcError as e:
                print("Adding scraper job failed: " + e.message)
                return None
    