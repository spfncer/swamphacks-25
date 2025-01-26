import os
from authlib.integrations.starlette_client import OAuth


"""Storing the configuration into the `auth0_config` variable for later usage"""
auth0_config = {
    "CLIENT_ID": os.getenv("AUTH0_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("AUTH0_CLIENT_SECRET"),
    "DOMAIN": os.getenv("AUTH0_DOMAIN"),
}

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid email profile",
        "timeout": 15.0,
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)
