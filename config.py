from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    def __init__(self):
        self.SCRAPER_HOST = os.getenv('SCRAPER_HOST', 'localhost')
        self.SCRAPER_PORT = os.getenv('SCRAPER_PORT', '50051')
        self.DATASTORE_HOST = os.getenv('DATASTORE_HOST', 'localhost')
        self.DATASTORE_PORT = os.getenv('DATASTORE_PORT', '50052')
        self.INDEX_HOST = os.getenv('INDEX_HOST', 'localhost')
        self.INDEX_PORT = os.getenv('INDEX_PORT', '50053')
        self.SEARCH_HOST = os.getenv('SEARCH_HOST', 'localhost')
        self.SEARCH_PORT = os.getenv('SEARCH_PORT', '50054')
        self.CHAT_HOST = os.getenv('CHAT_HOST', 'localhost')
        self.CHAT_PORT = os.getenv('CHAT_PORT', '50055')
        self.MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY', '')
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
        self.MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
        self.ZILLIZ_USER = os.getenv('ZILLIZ_USER', 'root')
        self.ZILLIZ_PASSWORD = os.getenv('ZILLIZ_PASSWORD', '')

config = Config()