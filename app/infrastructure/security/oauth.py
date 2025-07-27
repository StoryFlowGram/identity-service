from authlib.integrations.starlette_client import OAuth
from app.config.config import GOOGLE_CLIENT_ID, GOOGLE_SECRET_CLIENT_ID
from dotenv import load_dotenv

load_dotenv(override=True)

oauth_client_instance = OAuth()
oauth_client_instance.register(
    name="google",
    client_id = GOOGLE_CLIENT_ID,
    client_secret= GOOGLE_SECRET_CLIENT_ID,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    }
)