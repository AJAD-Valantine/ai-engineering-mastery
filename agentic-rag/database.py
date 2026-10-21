from config import get_settings
from pinecone import Pinecone

settings = get_settings()

pc = Pinecone(api_key=settings.pinecone_api_key.get_secret_value())
