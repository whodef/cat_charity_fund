from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings as s

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': s.type,
    'project_id': s.project_id,
    'private_key_id': s.private_key_id,
    'private_key': s.private_key,
    'client_id': s.client_id,
    'client_email': s.client_email,
    'auth_uri': s.auth_uri,
    'token_uri': s.token_uri,
    'client_x509_cert_url': s.client_x509_cert_url,
    'auth_provider_x509_cert_url': s.auth_provider_x509_cert_url
}

credentials = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    """
    Создаёт экземпляр класса Aiogoogle.

    ### Yields:
        Aiogoogle
    """
    async with Aiogoogle(service_account_creds=credentials) as aiogoogle:
        yield aiogoogle
