import os
import sys

# Add the 'gen' folder to the Python path for the current process only
gen_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gen'))
sys.path.insert(0, gen_folder)
import scraper_pb2, scraper_pb2_grpc

from concurrent import futures
import grpc

from service.scraper.scraper import Scraper


from config import config

class ScraperServicer(scraper_pb2_grpc.ScraperServicer):
    def __init__(self) -> None:
        super().__init__()
        self.scraper = Scraper()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scraper_pb2_grpc.add_ScraperServicer_to_server(ScraperServicer(), server)
    server.add_insecure_port(f'{config.SCRAPER_HOST}:{config.SCRAPER_PORT}')
    server.start()
    print(f"Scraper gRPC server running at {config.SCRAPER_HOST}:{config.SCRAPER_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    print("Starting Scraper gRPC server")
    serve()
