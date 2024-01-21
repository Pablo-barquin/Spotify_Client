from urllib.parse import urlencode

import secrets
import base64
import hashlib
import requests


class SpotifyClient:
    def __init__(self, client_id):
        self.client_id = client_id
        self.code_challenge = self._get_code_challenge()
        self.authorization = self._get_authorization_code()
        #self.access_token = self._get_access_token()

    def _get_code_challenge(self):
        # Sigue el metodo de autorización a través de PKCE
        verifier = self.__get_code_verifier()
        sha256 = hashlib.sha256(verifier.encode()).digest()

        return base64.urlsafe_b64encode(sha256).decode().rstrip('=')

    def _get_authorization_code(self):
        # Implementa la lógica para solicitar la autorización por parte del usuario
        url = "https://accounts.spotify.com/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": "http://localhost:8000",  
            "scope": "user-read-private user-read-email",  
            "code_challenge_method": "S256",
            "code_challenge": self.code_challenge
        }
        return f"{url}?{urlencode(params)}"


    def _get_access_token(self):
        # Implementa la lógica para obtener el token de acceso
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": "---"
        }
        response = requests.post(url=url, headers=headers, data=body, timeout=2.5)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error en la solicitud: {response.status_code} {response.text}")

    def __get_code_verifier(self):
        return secrets.token_urlsafe(64)

CLIENT_ID = '38fdfbab5c8247ee8736fd3147a00f50'

hola = SpotifyClient(CLIENT_ID)
print(hola.authorization)
