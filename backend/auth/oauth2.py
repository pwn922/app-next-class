from requests_oauthlib import OAuth2Session

from config.config import ConfigGoogle
from flask_restful import url_for, request
import requests
import jwt
from jwt.algorithms import RSAAlgorithm

import logging

logging.basicConfig(level=logging.INFO)

CLIENT_SECRET = ConfigGoogle.GOOGLE_CLIENT_SECRET
CLIENT_ID = ConfigGoogle.GOOGLE_CLIENT_ID
GOOGLE_SCOPES = ConfigGoogle.GOOGLE_SCOPES
GOOGLE_DISCOVERY_URL = ConfigGoogle.GOOGLE_DISCOVERY_URL


def create_oauth2_session(state=None):
    redirect_uri = request.host_url.removesuffix("/") + url_for("callback")
    return OAuth2Session(
            client_id=CLIENT_ID,
            scope=GOOGLE_SCOPES,
            redirect_uri=redirect_uri,
            state=state
    )


def get_openid_configuration():
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(
            f"HTTP error while fetching OpenID configuration: "
            f"{http_err}"
        )
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(
            f"Connection error while fetching OpenID "
            f"configuration: {conn_err}"
        )
    except requests.exceptions.Timeout as timeout_err:
        logging.error(
            f"Timeout error while fetching OpenID "
            f"configuration: {timeout_err}"
        )
    except requests.exceptions.RequestException as req_err:
        logging.error(
            f"RequestException while fetching OpenID "
            f"configuration: {req_err}"
        )
    except ValueError as json_err:
        logging.error(
            f"Error parsing JSON from OpenID configuration: "
            f"{json_err}"
        )
    return None


def verify_id_token(token):
    try:
        openid_conf = get_openid_configuration()

        # TODO - Buscar cómo cachear las keys
        logging.info(f"Token: {token}\n")
        jwks = requests.get(openid_conf["jwks_uri"], timeout=10).json()
        keys = jwks.get("keys", [])
        if not keys:
            return None

        # logging.info(f"Keys: {keys}")
        jwt_header = jwt.get_unverified_header(token)
        kid = jwt_header.get('kid', '')
        if not kid:
            return None

        jwk_data = next((k for k in keys if k['kid'] == kid), '')
        if not jwk_data:
            return None

        logging.info(f"JWK: {jwk_data}\n")
        public_key = RSAAlgorithm.from_jwk(jwk_data)

        logging.info(f"Public Key: {public_key}\n")
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )

        iss_token = decoded_token.get('iss')
        GOOGLE_DOMAINS = [
            "https://accounts.google.com",
            "accounts.google.com"
        ]

        if iss_token not in GOOGLE_DOMAINS:
            return None

        return decoded_token

    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
        return None

    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token!: {e}\n")
        return None

    except Exception as e:
        logging.exception(f"Unexpected error verifying token: {e}")
        return None
