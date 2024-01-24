import secrets
import base64
import hashlib
import requests


class SpotifyClient:
    '''Contiene todas las funciones relacionadas con las llamadas a la API de Spotify'''
    def __init__(self):
        self.client_id = '38fdfbab5c8247ee8736fd3147a00f50'
        self.redirect_uri = "http://localhost:8000/callback"
        self.scope = "user-read-private user-read-email user-top-read user-read-recently-played"
        self.code_verifier = self.__get_code_verifier()
        self.code_challenge = self.get_code_challenge()

    def __get_code_verifier(self):
        '''Funciona como "Code Verifier" dentro del estandar PKCE'''
        return secrets.token_urlsafe(64)

    def get_code_challenge(self):
        '''Funciona como "Code Challenge" dentro del flujo de autentificación PKCE'''
        verifier = self.code_verifier
        print(verifier)
        sha256 = hashlib.sha256(verifier.encode()).digest()

        return base64.urlsafe_b64encode(sha256).decode().rstrip('=')

    def get_access_token(self, code, code_verifier):
        '''Implementa la lógica para obtener el token de acceso'''
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8000/callback",
            "client_id": self.client_id,
            "code_verifier": code_verifier
        }
        response = requests.post(url=url, headers=headers, data=body, timeout=5)

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return {"error": f'Error al obtener el token de acceso: {response.status_code} {response.text}'}

    def get_spotify_user_profile(self, access_token):
        '''Obtiene el perfil del usuario de Spotify utilizando el token de acceso.'''
        url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            return response.json()  # Retorna la información del perfil del usuario
        else:
            return {"error": f"Error al obtener el perfil del usuario: {response.status_code}"}
    
    def get_spotify_recently_tracks(self, access_token):
        '''Obtiene las canciones más escuchadas en las últimas 4 semanas por el usuario utilizando el token de acceso.'''
        url = "https://api.spotify.com/v1/me/top/tracks"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"time_range": "short_term"}
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            return response.json()  # Retorna las canciones escuchadas 
        else:
            return {"error": f"Error las canciones escuchadas: {response.status_code}"}